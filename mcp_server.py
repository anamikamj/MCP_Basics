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

@mcp.tool()
def count_words(file_name: str) -> int:
    """
    Count words in a markdown file
    """

    path=os.path.join(MARKDOWN_FOLDER,file_name)
    with open(path,"r",encoding="utf-8") as file:
        text=file.read()
    return len(text.split())

@mcp.tools()
def extract_headings(file_name :str) ->list:
    """extracting headings in a file"""
    path=os.path.join(MARKDOWN_FOLDER,file_name)
    with open(path,"r",encoding="utf-8") as file:
        lines=file.readlines()
    headings=[]
    for line in lines:
        if line.startswith("#"):
            headings.append(line.strip())
    return headings

if __name__ == "__main__":
    mcp.run()