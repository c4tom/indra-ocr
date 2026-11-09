"""Run Indra OCR as a local MCP server over Streamable HTTP."""

from __future__ import annotations

from pathlib import Path

import indra_ocr
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Indra OCR", stateless_http=True)
DOCUMENTS = Path("/documents").resolve()


@mcp.tool(description="OCR a PDF or image in /documents and return markdown output.")
def ocr_document(filename: str, max_pages: int = 20) -> str:
    """OCR a document stored in the mounted /documents directory."""
    if not 1 <= max_pages <= 100:
        raise ValueError("max_pages must be between 1 and 100")

    path = (DOCUMENTS / filename).resolve()
    if not path.is_relative_to(DOCUMENTS):
        raise ValueError("filename must stay inside /documents")
    if not path.is_file():
        raise ValueError(f"{filename!r} was not found in /documents")

    converter = indra_ocr.load(threads=4)
    pages: list[str] = []
    for _, page in converter.convert(path, max_pages=max_pages):
        if page.source == "error":
            raise ValueError(f"OCR failed for {filename}: {page.note}")
        text = page.markdown if page.markdown is not None else page.text
        if text:
            pages.append(text)

    return "\n\n".join(pages)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(mcp.streamable_http_app(), host="0.0.0.0", port=8000)
