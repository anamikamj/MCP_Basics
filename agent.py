"""
AGENT
Workflow:
1.Connect to MCP Server
2.call read_markdown tool
3.Get markdown content
4.Send content to Gemini
5.Print summary
"""
import asyncio #Used for asynchronous programming.
#multiple tasks at a time--mcp server runs in background and other tasks continue
import os #Used for environment variables.
from dotenv import load_dotenv #for loading api key from .env
from mcp import ClientSession #ClientSession is the connection btw Agent and MCP Server
from mcp.client.stdio import stdio_client,StdioServerParameters
#stdio: (transport methods-stdio used to do everthing in terminal,http--to connect to cloud like google,aws)
#Agent->stdin->Server , Server->stdout->Agent
#StdioServerParameters:
#Tells MCP Which server should I start?
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate #reusable prompts , it is more structured

load_dotenv() #loads API key into memory

llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)#for summarization better temp=0

async def main():
    server_params=StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    ) #means python mcp_server.py
    #just combine command+args
    #so python automatically starts mcp_server.py
    async with stdio_client(server_params) as (
        read_stream,
        write_stream
    ): #creates 2 communication channel btw agent and server,so we hv 2 pipies
        #read_stream=receives data (Server to Agent)
        ##write_stream=sends data Agents to Server
        async with ClientSession(
            read_stream,
            write_stream
        ) as session: #ClientSession starts an actual MCP Session Now both sides can talk.
            await session.initialize()
            #performs MCP handshake:
            #Client:Hello and Server also says:Hello
            print("Connected to MCP Server")

            #get available markdowns
            files=await session.call_tool(
                "list_markdowns",{} #reqd tool in mcp_server
            )

            print("Available Markdown Files:\n")

            for file in files.content:
                print(file.text)

            '''
            content=[
    TextContent(text="apisinfo.md"),
    TextContent(text="contributerinfo.md"),
    TextContent(text="notes.md")
]
            '''

            print()

            selected_file = input(
                "Enter filename: "
            )

            #to choose the reqd mcp tool:summarise/count/extract headings
            print("\nChoose Operation:\n")
            print("1. Summarize")
            print("2. Count Words")
            print("3. Extract Headings")

            choice = int(input("\nEnter choice: "))

            if choice==1:
                result=await session.call_tool(
                    "read_markdown", #reqd tool in mcp_server
                    {
                        "file_name":selected_file
                    }
                )

                ''''
                Client sends:{
                "tool":"read_markdown", "file_path":"notes.md"}
                to MCP server.
                '''

                #print(result)

                ''''
                result is of the form:
                result = CallToolResult(
        content=[
            TextContent(
                text="# Artificial Intelligence\nAI is ..."
            )
        ]
    ) #since content is a list--content[0]
                '''

                markdown_content=result.content[0].text
                print("Markdown received")

                prompt=ChatPromptTemplate.from_template(
                    """
                    Summarize the following markdown content.
                    Markdown:
                    {content}
                    """
                )

                chain=prompt|llm

                ''''
                output of prompt goes into LLM
                '''

                response=chain.invoke(
                    {
                        "content": markdown_content
                    }
                )

                #langchain replaces content with markdown_content then sends full prompt to gemini
                print("\nSUMMARY\n")
                print(response.content)

            elif choice==2:
                result = await session.call_tool(
                    "count_words",
                    {
                        "file_name": selected_file
                    }
                )

                print(
                    "\nWord Count:",
                    result.content[0].text
                )

            elif choice==3:
                result = await session.call_tool(
                    "extract_headings",
                    {
                        "file_name": selected_file
                    }
                )

                print("\nHeadings:\n")

                for heading in result.content:
                    print(heading.text)


if __name__=="__main__":
    ''''
    Runs code only when file is executed directly.Example:python agent.py-->True.
    Example:import agent-->False.
    '''
    asyncio.run(main()) #runs async function