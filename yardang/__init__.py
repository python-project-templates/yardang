__version__ = "0.5.0"

from .build import generate_docs_configuration, generate_wiki_configuration, run_doxygen_if_needed
from .wiki import process_wiki_output

__all__ = (
    "generate_docs_configuration",
    "generate_wiki_configuration",
    "run_doxygen_if_needed",
    "process_wiki_output",
)
