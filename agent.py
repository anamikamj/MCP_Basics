"""
AGENT
workflow:
1.Connect to mcp server
2. call read_markdown tool
3. get markdown content
4. send content to gemini
5. Print summary
"""
#used for the asynchronous programming ie multiple tasks run at the time
import asyncio

#the mcp will run in the background and other tasks continue
import os

from dotenv import load_dotenv

from mcp import ClientSession

#stdioclient is for agent->stdin->server and server->stdout->agent
from mcp.client.stdio import stdio_client
from mcp.client.stdio import StdioServerParameters#tells which mcp server to be started with
from langchain_google_genai import ChatGoogleGenerativeAI
#used for the prompt writing
from langchain_core.prompts import ChatPromptTemplate

#load api kety to memory
load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)

async def main():
    server_params=StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )#means python mcp_server.py
    async with stdio_client(server_params) as(
        read_stream,
        write_stream
    ):
        #this will create 2 comm channel between the agent and server hence there will be 2 pipes
        async with ClientSession(
            read_stream,#stdin (receices data ie from server to agent)
            write_stream #stdout (send data ie from agents to server)
        ) as session: #starts actual mcp session
            
            #performs mcp handshake between client and server 
            await session.initialize()
            print("Connected to MCP server")

            #the client will send the tool to be used as read_markdown and filepath as notes.md
            result=await session.call_tool(
                "read_markdown",
                {
                    "file_path":"notes.md"
                }
            )
            
            #result will be having a content and content is a list 
            '''result = CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text="# My Markdown Notes\n..."
                    )
                ]
            )
            '''
            markdown_content=result.content[0].text
            print("Markdown received")

            prompt=ChatPromptTemplate.from_template(
                """
                Summarize the following markdown content.

                Markdown:
                {content}#this is a placeholder whose value will be given during the invoke
                """
            )

            #output of the prompt goes into the llm (gemini)
            chain = prompt | llm
            #placeholder of the prompt will be having the markdown_content
            response=chain.invoke(
                {
                    "content":markdown_content
                }
            )

            print("\nSummary\n")
            print(response.content)

#this allows the file to be only executed directly ie by using python agent.py and does not allow import agent  
if __name__=="__main__":
    asyncio.run(main())
