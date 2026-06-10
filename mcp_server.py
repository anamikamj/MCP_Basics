from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("MarkdownServer")

MARKDOWN_FOLDER = "markdowns"


@mcp.tool()
def list_markdowns() -> list:
    """
    Return all markdown files available.
    """

    return [
        file
        for file in os.listdir(MARKDOWN_FOLDER)
        if file.endswith(".md")
    ]


@mcp.tool()
def read_markdown(file_name: str) -> str:
    """
    Read a markdown file.
    """

    file_path = os.path.join(
        MARKDOWN_FOLDER,
        file_name
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


if __name__ == "__main__":
    mcp.run()