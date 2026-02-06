"""GitHub Wiki markdown generation and post-processing.

This module provides functionality to generate GitHub Wiki compatible markdown
from Sphinx documentation using sphinx-markdown-builder, with post-processing
to create proper sidebar navigation and fix internal links.
"""

import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple

__all__ = (
    "generate_sidebar",
    "generate_footer",
    "fix_wiki_links",
    "process_wiki_output",
    "get_page_title",
)


def get_page_title(filepath: Path) -> str:
    """Extract the title from a markdown file.

    Looks for the first H1 heading (# Title) in the file.
    Falls back to the filename without extension.

    Args:
        filepath: Path to the markdown file.

    Returns:
        The extracted title or filename-based title.
    """
    try:
        content = filepath.read_text(encoding="utf-8")
        # Look for first H1 heading
        match = re.search(r"^#\s+(.+?)(?:\s*\{.*\})?$", content, re.MULTILINE)
        if match:
            title = match.group(1).strip()
            # Remove any remaining markdown formatting
            title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title)
            title = re.sub(r"`([^`]+)`", r"\1", title)
            return title
    except Exception:
        pass

    # Fallback to filename
    name = filepath.stem
    # Convert Home or index to Home
    if name.lower() in ("index", "readme"):
        return "Home"
    # Convert kebab-case or snake_case to Title Case
    name = name.replace("-", " ").replace("_", " ")
    return name.title()


def convert_filename_to_wiki_format(filename: str) -> str:
    """Convert a filename to GitHub Wiki format.

    GitHub Wiki uses spaces in URLs which map to filenames with hyphens or spaces.
    We'll use the standard approach of keeping the filename but fixing the extension.

    Args:
        filename: Original filename (may include path components).

    Returns:
        Wiki-compatible filename.
    """
    # Remove path components for wiki (wiki is flat)
    name = Path(filename).stem
    # Handle index/readme -> Home
    if name.lower() in ("index", "readme"):
        return "Home"
    return name


def fix_wiki_links(content: str, all_pages: Dict[str, str]) -> str:
    """Fix internal links to use GitHub Wiki format.

    Converts relative markdown links to GitHub Wiki internal links.
    GitHub Wiki links use [[Page Name]] or [text](Page-Name) format.

    Args:
        content: Markdown content to process.
        all_pages: Dict mapping original paths to wiki page names.

    Returns:
        Content with fixed links.
    """

    # Fix standard markdown links [text](path)
    def replace_link(match):
        text = match.group(1)
        path = match.group(2)

        # Skip external links
        if path.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)

        # Handle anchor links within same page
        if path.startswith("#"):
            return match.group(0)

        # Extract path and anchor
        anchor = ""
        if "#" in path:
            path, anchor = path.split("#", 1)
            anchor = "#" + anchor

        # Remove .md extension if present
        if path.endswith(".md"):
            path = path[:-3]

        # Convert path to wiki page name
        page_name = convert_filename_to_wiki_format(path)

        # Check if it's a known page
        for orig_path, wiki_name in all_pages.items():
            if path in orig_path or orig_path.endswith(path):
                page_name = wiki_name
                break

        return f"[{text}]({page_name}{anchor})"

    content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, content)

    return content


def cleanup_markdown(content: str) -> str:
    """Clean up markdown content for better GitHub Wiki rendering.

    Fixes common issues from sphinx-markdown-builder output:
    - Expands collapsed HTML tags onto multiple lines
    - Removes anchor tags before headings
    - Fixes collapsed badge lines
    - Fixes collapsed code blocks
    - Reduces large image sizes
    - Cleans up extra whitespace

    Args:
        content: Raw markdown content.

    Returns:
        Cleaned markdown content.
    """
    # Remove anchor tags before headings (e.g., <a id="overview"></a>)
    content = re.sub(r'<a id="[^"]+"></a>\s*\n?', "", content)

    # Reduce image widths by 50% for wiki (GitHub wiki renders larger)
    def reduce_image_width(match):
        width = int(match.group(1))
        new_width = max(16, width // 2)  # Reduce by 50%, minimum 16px
        return f'width="{new_width}"'

    content = re.sub(r'width="(\d+)"', reduce_image_width, content)

    # Fix collapsed div tags - add newlines after > and before <
    # Match: <div ...>   content   </div> and expand it
    def expand_div(match):
        full = match.group(0)
        # Add newlines for readability
        full = re.sub(r">\s+<", ">\n<", full)
        return full

    content = re.sub(r"<div[^>]*>.*?</div>", expand_div, content, flags=re.DOTALL)

    # Fix collapsed badge lines - ensure badges are on separate lines
    # Match multiple consecutive badges and separate them
    content = re.sub(r"\]\)\s*\[!\[", "])\n\n[![", content)

    # Fix collapsed code blocks - the sphinx-markdown-builder collapses
    # multi-line code into single lines with multiple spaces
    def fix_code_block(match):
        lang = match.group(1) or ""
        code = match.group(2)

        # Replace 2+ spaces with newlines, being careful about context
        # First, handle obvious statement boundaries

        # Python: statement followed by spaces then new statement
        code = re.sub(
            r"([\)\]\"\'])\s{2,}(def |class |import |from |with |if |elif |else:|for |while |return |raise |try:|except|finally:|#|@\w)",
            r"\1\n\2",
            code,
        )

        # Python: assignment or call followed by new statement
        code = re.sub(r"(\w)\s{2,}(def |class |import |from |with |if |for |while |return |#)", r"\1\n\2", code)

        # YAML: value followed by new key at same or lower indent level
        code = re.sub(r"(\]|\"|\'|\w)\s{2,}(\w+:)", r"\1\n\2", code)

        # YAML: list item followed by another list item or key
        code = re.sub(r"(-\s+\S[^\n]*)\s{2,}(-\s+|\w+:)", r"\1\n\2", code)

        # Generic: detect lines that got merged (4+ spaces often indicates this)
        code = re.sub(r"(\S)\s{4,}(\S)", r"\1\n\2", code)

        return f"```{lang}\n{code}\n```"

    content = re.sub(r"```(\w*)\n?(.*?)\n?```", fix_code_block, content, flags=re.DOTALL)

    # Remove excessive blank lines (more than 2)
    content = re.sub(r"\n{4,}", "\n\n\n", content)

    # Clean up lines that are just whitespace
    content = re.sub(r"\n[ \t]+\n", "\n\n", content)

    return content


def extract_toctree_entries(content: str) -> List[Tuple[str, str]]:
    """Extract toctree entries from markdown content.

    Parses MyST-style toctree directives to find linked pages.

    Args:
        content: Markdown content with toctree directives.

    Returns:
        List of (title, path) tuples for toctree entries.
    """
    entries = []

    # Match MyST toctree blocks
    toctree_pattern = r"```\{toctree\}.*?```"
    matches = re.findall(toctree_pattern, content, re.DOTALL)

    for toctree_block in matches:
        # Extract entries from toctree block
        lines = toctree_block.split("\n")
        in_content = False
        for line in lines:
            line = line.strip()
            # Skip directive header and options
            if line.startswith("```") or line.startswith(":") or line.startswith("---"):
                if line == "---":
                    in_content = True
                continue
            if not in_content and line.startswith(":"):
                continue
            if line.startswith("---"):
                in_content = True
                continue
            if in_content and line and not line.startswith(":"):
                # This is an entry
                path = line.strip()
                if path:
                    entries.append((None, path))

    return entries


def generate_sidebar(
    output_dir: Path,
    pages: List[str],
    project_name: str = "",
    *,
    include_home: bool = True,
    include_extra_pages: bool = False,
) -> str:
    """Generate a _Sidebar.md file for GitHub Wiki.

    Creates a sidebar navigation file based on the documentation structure.

    Args:
        output_dir: Directory containing the markdown output.
        pages: List of page paths from the yardang configuration.
        project_name: Project name for the sidebar header.
        include_home: Whether to include a Home link at the top.
        include_extra_pages: Whether to include pages not in the explicit list.

    Returns:
        The generated sidebar content.
    """
    lines = []

    # Patterns to exclude from sidebar (internal/generated pages)
    exclude_patterns = [
        ".github-",
        "api-crates-",
        "docs-src-",
        "docs-notebooks-",
        "examples-",
        ".doctrees",
        "_static",
        "_sphinx",
    ]

    if project_name:
        lines.append(f"### {project_name}")
        lines.append("")

    if include_home:
        lines.append("* [Home](Home)")

    # Track what we've added
    added_pages = {"home"}

    # Build navigation from explicit pages list
    for page_path in pages:
        # Get the wiki filename - try to match the flattened name
        wiki_name = convert_filename_to_wiki_format(page_path)

        # Also try the flattened format (docs-src-overview instead of overview)
        flattened_name = page_path.replace("/", "-").replace(".md", "")
        if flattened_name.startswith("docs-src-"):
            flattened_name = flattened_name[9:]  # Remove docs-src- prefix for cleaner names

        # Try to find the file - check both formats
        md_file = None
        actual_wiki_name = wiki_name
        for candidate in [wiki_name, flattened_name, f"docs-src-{wiki_name}"]:
            candidate_file = output_dir / f"{candidate}.md"
            if candidate_file.exists():
                md_file = candidate_file
                actual_wiki_name = candidate
                break

        if md_file and md_file.exists():
            title = get_page_title(md_file)
        else:
            title = wiki_name.replace("-", " ").replace("_", " ").title()

        lines.append(f"* [{title}]({actual_wiki_name})")
        added_pages.add(actual_wiki_name.lower())
        added_pages.add(wiki_name.lower())

    # Optionally check for additional pages not in the explicit list
    if include_extra_pages:
        for md_file in sorted(output_dir.glob("*.md")):
            if md_file.name.startswith("_"):
                continue

            wiki_name = md_file.stem

            # Skip if matches exclude patterns
            should_skip = any(pattern in wiki_name.lower() for pattern in exclude_patterns)
            if should_skip:
                continue

            if wiki_name.lower() in added_pages:
                continue

            title = get_page_title(md_file)
            lines.append(f"* [{title}]({wiki_name})")
            added_pages.add(wiki_name.lower())

    content = "\n".join(lines)

    # Write the sidebar file
    sidebar_file = output_dir / "_Sidebar.md"
    sidebar_file.write_text(content, encoding="utf-8")

    return content


def generate_footer(
    output_dir: Path,
    project_name: str = "",
    docs_url: str = "",
    repo_url: str = "",
) -> str:
    """Generate a _Footer.md file for GitHub Wiki.

    Creates a footer with links to the main documentation and repository.

    Args:
        output_dir: Directory containing the markdown output.
        project_name: Project name.
        docs_url: URL to the main documentation site.
        repo_url: URL to the repository.

    Returns:
        The generated footer content.
    """
    lines = ["---", ""]

    links = []
    if docs_url:
        links.append(f"[📚 Full Documentation]({docs_url})")
    if repo_url:
        links.append(f"[💻 Repository]({repo_url})")

    if links:
        lines.append(" | ".join(links))
    else:
        lines.append(f"*Generated from {project_name} documentation*")

    content = "\n".join(lines)

    # Write the footer file
    footer_file = output_dir / "_Footer.md"
    footer_file.write_text(content, encoding="utf-8")

    return content


def rename_index_to_home(output_dir: Path) -> None:
    """Rename index.md to Home.md for GitHub Wiki.

    GitHub Wiki uses Home.md as the landing page.

    Args:
        output_dir: Directory containing the markdown output.
    """
    index_file = output_dir / "index.md"
    home_file = output_dir / "Home.md"

    if index_file.exists() and not home_file.exists():
        shutil.move(str(index_file), str(home_file))


def flatten_directory_structure(output_dir: Path, max_filename_length: int = 200) -> Dict[str, str]:
    """Flatten nested directory structure for GitHub Wiki.

    GitHub Wiki doesn't support nested directories, so we need to
    flatten the structure and rename files appropriately.

    Args:
        output_dir: Directory containing the markdown output.
        max_filename_length: Maximum length for generated filenames.

    Returns:
        Dict mapping original paths to new wiki page names.
    """
    page_map = {}

    # Patterns to skip (these are build artifacts, not documentation)
    skip_patterns = ["jupyter_execute", "_build", ".ipynb_checkpoints", "__pycache__"]

    # Find all markdown files recursively
    for md_file in output_dir.rglob("*.md"):
        # Skip files in directories matching skip patterns
        rel_path = md_file.relative_to(output_dir)
        should_skip = any(pattern in str(rel_path) for pattern in skip_patterns)
        if should_skip:
            # Remove these files as they're build artifacts
            try:
                md_file.unlink()
            except OSError:
                pass
            continue

        if md_file.parent == output_dir:
            # Already at top level
            wiki_name = md_file.stem
            if wiki_name.lower() in ("index", "readme"):
                wiki_name = "Home"
            page_map[str(rel_path)] = wiki_name
            continue

        # Build a flattened name from the path
        parts = list(rel_path.parts)

        # Remove 'index.md' at the end and use parent name
        if parts[-1].lower() in ("index.md", "readme.md"):
            parts = parts[:-1]
            if parts:
                wiki_name = "-".join(parts)
            else:
                wiki_name = "Home"
        else:
            # Remove .md extension
            parts[-1] = Path(parts[-1]).stem
            wiki_name = "-".join(parts)

        # Truncate if name is too long (with room for .md extension)
        if len(wiki_name) > max_filename_length:
            # Use hash to make unique truncated name
            import hashlib

            name_hash = hashlib.md5(wiki_name.encode()).hexdigest()[:8]
            wiki_name = wiki_name[: max_filename_length - 10] + "-" + name_hash

        page_map[str(rel_path)] = wiki_name

        # Move file to top level with new name
        new_path = output_dir / f"{wiki_name}.md"
        if not new_path.exists():
            try:
                shutil.move(str(md_file), str(new_path))
            except OSError:
                # Skip files that can't be moved (e.g., name too long on some systems)
                pass

    # Remove empty directories
    for subdir in sorted(output_dir.rglob("*"), reverse=True):
        if subdir.is_dir():
            try:
                if not any(subdir.iterdir()):
                    subdir.rmdir()
            except OSError:
                pass

    return page_map


def process_wiki_output(
    output_dir: Path,
    pages: Optional[List[str]] = None,
    project_name: str = "",
    docs_url: str = "",
    repo_url: str = "",
    *,
    generate_sidebar_file: bool = True,
    generate_footer_file: bool = True,
    fix_links: bool = True,
) -> None:
    """Process sphinx-markdown-builder output for GitHub Wiki compatibility.

    This is the main entry point for wiki post-processing. It:
    1. Flattens the directory structure
    2. Renames index.md to Home.md
    3. Fixes internal links
    4. Generates _Sidebar.md
    5. Generates _Footer.md

    Args:
        output_dir: Directory containing the markdown output from sphinx-markdown-builder.
        pages: List of page paths from the yardang configuration.
        project_name: Project name for sidebar/footer.
        docs_url: URL to the main documentation site.
        repo_url: URL to the repository.
        generate_sidebar_file: Whether to generate _Sidebar.md.
        generate_footer_file: Whether to generate _Footer.md.
        fix_links: Whether to fix internal links.
    """
    output_dir = Path(output_dir)
    pages = pages or []

    if not output_dir.exists():
        raise FileNotFoundError(f"Output directory not found: {output_dir}")

    # Flatten directory structure
    page_map = flatten_directory_structure(output_dir)

    # Rename index to Home
    rename_index_to_home(output_dir)

    # Update page map for Home
    for orig_path, wiki_name in list(page_map.items()):
        if wiki_name.lower() in ("index", "readme"):
            page_map[orig_path] = "Home"

    # Fix links in all markdown files
    if fix_links:
        for md_file in output_dir.glob("*.md"):
            if md_file.name.startswith("_"):
                continue

            content = md_file.read_text(encoding="utf-8")
            # Clean up markdown formatting issues
            content = cleanup_markdown(content)
            # Fix internal links for wiki
            fixed_content = fix_wiki_links(content, page_map)
            md_file.write_text(fixed_content, encoding="utf-8")

    # Generate sidebar
    if generate_sidebar_file:
        generate_sidebar(output_dir, pages, project_name)

    # Generate footer
    if generate_footer_file:
        generate_footer(output_dir, project_name, docs_url, repo_url)
