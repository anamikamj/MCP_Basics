"""
MCP SERVER
This mcp server is used for reading a markdown file and return its summarized contents
"""

from mcp.server.fastmcp import FastMCP

#creating the mcp server
mcp=FastMCP("MarkdownServer") #MarkdownServer is the name of the server created

@mcp.tool() #only if we create the tool for the fn it will be available to the MCPclient
def read_markdown(file_path:str)->str:
    """"
    Read a markdown file
    args:
        file_path:Path to the markdown file
    returns:
        markdown content as atring
    """
    with open(file_path,"r",encoding="utf-8") as file:
        content=file.read()
    return content


#starting the mcp server
if __name__=="__main__":
    mcp.run()