import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

_MARKDOWN_LINK = re.compile(
    r"(?P<prefix>!?\[[^\]\n]*\]\(\s*)"
    r"(?:<(?P<angle_url>[^>\n]+)>|(?P<url>[^<>\s)]+))"
    r"(?P<suffix>(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^\)\n]*\)))?\s*\))"
)
_REFERENCE_DEFINITION = re.compile(
    r"^(?P<prefix>[ \t]{0,3}\[[^\]\n]+\]:[ \t]*)"
    r"(?:<(?P<angle_url>[^>\n]+)>|(?P<url>[^<>\s]+))"
    r"(?P<suffix>(?:[ \t]+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^\)\n]*\)))?[ \t]*)$",
    re.MULTILINE,
)
_HTML_ATTRIBUTE = re.compile(
    r"(?P<prefix>(?<![\w:-])(?:href|src)\s*=\s*)"
    r"(?:(?P<quote>[\"'])(?P<quoted_url>.*?)(?P=quote)|(?P<unquoted_url>[^\s\"'=<>`]+))",
    re.IGNORECASE,
)
_HTML_SRCSET = re.compile(
    r"(?P<prefix>(?<![\w:-])srcset\s*=\s*)"
    r"(?:(?P<quote>[\"'])(?P<quoted_value>.*?)(?P=quote)|(?P<unquoted_value>[^\s\"'=<>`]+))",
    re.IGNORECASE,
)
_FENCE_OPEN = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})")
_PROTECTED_INLINE = re.compile(r"<!--.*?-->|(?<!`)(?P<ticks>`+)(?!`).*?(?<!`)(?P=ticks)(?!`)", re.DOTALL)


def _rebase_url(url: str, source_dir: str, destination_dir: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
        return url

    source_path = posixpath.normpath(posixpath.join(source_dir, parsed.path))
    rebased_path = posixpath.relpath(source_path, destination_dir)
    return urlunsplit(("", "", rebased_path, parsed.query, parsed.fragment))


def _replace_url_group(match: re.Match, source_dir: str, destination_dir: str) -> str:
    group = "angle_url" if match.groupdict().get("angle_url") is not None else "url"
    url = _rebase_url(match.group(group), source_dir, destination_dir)
    value = match.group(0)
    start = match.start(group) - match.start()
    end = match.end(group) - match.start()
    return f"{value[:start]}{url}{value[end:]}"


def _fenced_segments(content: str):
    lines = content.splitlines(keepends=True)
    active_lines = []
    protected_lines = []
    fence_character = ""
    fence_length = 0

    for line in lines:
        if protected_lines:
            protected_lines.append(line)
            closing = line.lstrip(" ")
            if len(line) - len(closing) <= 3:
                closing = closing.rstrip("\r\n")
                delimiter_length = len(closing) - len(closing.lstrip(fence_character))
                if delimiter_length >= fence_length and not closing[delimiter_length:].strip():
                    yield "".join(protected_lines), False
                    protected_lines = []
            continue

        opening = _FENCE_OPEN.match(line)
        if opening:
            if active_lines:
                yield "".join(active_lines), True
                active_lines = []
            fence = opening.group("fence")
            fence_character = fence[0]
            fence_length = len(fence)
            protected_lines = [line]
        else:
            active_lines.append(line)

    if protected_lines:
        yield "".join(protected_lines), False
    if active_lines:
        yield "".join(active_lines), True


def _content_segments(content: str):
    for segment, active in _fenced_segments(content):
        if not active:
            yield segment, False
            continue

        position = 0
        for match in _PROTECTED_INLINE.finditer(segment):
            if match.start() > position:
                yield segment[position : match.start()], True
            yield match.group(0), False
            position = match.end()
        if position < len(segment):
            yield segment[position:], True


def _transform_active_content(content: str, transform) -> str:
    return "".join(transform(segment) if active else segment for segment, active in _content_segments(content))


def _rebase_markdown_links(content: str, source_dir: str, destination_dir: str) -> str:
    def replace(match: re.Match) -> str:
        return _replace_url_group(match, source_dir, destination_dir)

    return _transform_active_content(content, lambda segment: _MARKDOWN_LINK.sub(replace, segment))


def _rebase_reference_definitions(content: str, source_dir: str, destination_dir: str) -> str:
    def replace(match: re.Match) -> str:
        return _replace_url_group(match, source_dir, destination_dir)

    return _transform_active_content(content, lambda segment: _REFERENCE_DEFINITION.sub(replace, segment))


def _srcset_url_spans(value: str):
    position = 0
    while position < len(value):
        while position < len(value) and (value[position].isspace() or value[position] == ","):
            position += 1
        start = position
        while position < len(value) and not value[position].isspace():
            position += 1
        end = position
        if start == end:
            break

        while end > start and value[end - 1] == ",":
            end -= 1
        has_separator = end < position
        if end > start:
            yield start, end
        if has_separator:
            continue

        parentheses = 0
        while position < len(value):
            character = value[position]
            if character == "(":
                parentheses += 1
            elif character == ")" and parentheses:
                parentheses -= 1
            elif character == "," and not parentheses:
                position += 1
                break
            position += 1


def _rebase_srcset(value: str, source_dir: str, destination_dir: str) -> str:
    result = []
    position = 0
    for start, end in _srcset_url_spans(value):
        result.append(value[position:start])
        result.append(_rebase_url(value[start:end], source_dir, destination_dir))
        position = end
    result.append(value[position:])
    return "".join(result)


def _rebase_html_attributes(content: str, source_dir: str, destination_dir: str) -> str:
    def replace_url(match: re.Match) -> str:
        group = "quoted_url" if match.group("quoted_url") is not None else "unquoted_url"
        url = _rebase_url(match.group(group), source_dir, destination_dir)
        value = match.group(0)
        start = match.start(group) - match.start()
        end = match.end(group) - match.start()
        return f"{value[:start]}{url}{value[end:]}"

    def replace_srcset(match: re.Match) -> str:
        group = "quoted_value" if match.group("quoted_value") is not None else "unquoted_value"
        srcset = _rebase_srcset(match.group(group), source_dir, destination_dir)
        value = match.group(0)
        start = match.start(group) - match.start()
        end = match.end(group) - match.start()
        return f"{value[:start]}{srcset}{value[end:]}"

    def transform(segment: str) -> str:
        segment = _HTML_ATTRIBUTE.sub(replace_url, segment)
        return _HTML_SRCSET.sub(replace_srcset, segment)

    return _transform_active_content(content, transform)


def _relative_html_urls(content: str):
    for segment, active in _content_segments(content):
        if not active:
            continue
        for match in _HTML_ATTRIBUTE.finditer(segment):
            group = "quoted_url" if match.group("quoted_url") is not None else "unquoted_url"
            yield match.group(group)
        for match in _HTML_SRCSET.finditer(segment):
            group = "quoted_value" if match.group("quoted_value") is not None else "unquoted_value"
            value = match.group(group)
            for start, end in _srcset_url_spans(value):
                yield value[start:end]


def copy_relative_html_assets(content: str, source: Path, destination: Path, output_dir: Path) -> None:
    """Copy local files referenced by raw HTML into the generated site."""
    source_dir = source.parent.as_posix()
    destination_dir = destination.parent.as_posix()
    output_root = output_dir.resolve()

    for url in _relative_html_urls(content):
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
            continue

        source_path = (source.parent / unquote(parsed.path)).resolve()
        rebased = urlsplit(_rebase_url(url, source_dir, destination_dir))
        output_path = (output_root / unquote(rebased.path)).resolve()
        if not source_path.is_file() or not output_path.is_relative_to(output_root):
            continue

        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, output_path)


def rebase_relative_references(content: str, source: Path, destination: Path) -> str:
    """Rebase relative Markdown and HTML references after moving content."""
    source_dir = source.parent.as_posix()
    destination_dir = destination.parent.as_posix()
    content = _rebase_markdown_links(content, source_dir, destination_dir)
    content = _rebase_reference_definitions(content, source_dir, destination_dir)
    return _rebase_html_attributes(content, source_dir, destination_dir)
