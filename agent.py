import asyncio
import os

from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters
)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )

    async with stdio_client(
        server_params
    ) as (
        read_stream,
        write_stream
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            print("\nConnected to MCP Server\n")

            # ------------------------
            # Get available markdowns
            # ------------------------

            files = await session.call_tool(
                "list_markdowns",
                {}
            )

            print("Available Markdown Files:\n")
            for file in files.content:
                print(file.text)

        

            selected_file = input(
                "Enter filename: "
            )

            # ------------------------
            # Read markdown
            # ------------------------

            result = await session.call_tool(
                "read_markdown",
                {
                    "file_name": selected_file
                }
            )

            markdown_content = (
                result.content[0].text
            )

            print(
                "\nMarkdown Loaded Successfully\n"
            )

            # ------------------------
            # Summarize
            # ------------------------

            prompt = ChatPromptTemplate.from_template(
                """
                Summarize the following markdown.

                Markdown:
                {content}
                """
            )

            chain = prompt | llm

            response = chain.invoke(
                {
                    "content": markdown_content
                }
            )

            print("\nSUMMARY\n")
            print(response.content)


if __name__ == "__main__":
    asyncio.run(main())