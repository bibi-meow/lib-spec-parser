"""Format detector: determines file format from path extension."""

import os


def detect_format(path: str) -> str:
    """Detect the file format based on file extension.

    Returns:
        "markdown" | "yaml" | "rst"
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in (".yaml", ".yml"):
        return "yaml"
    if ext == ".rst":
        return "rst"
    return "markdown"
