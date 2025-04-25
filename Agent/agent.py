import streamlit as st

st.set_page_config(
    page_title="Web Research Agent",
    page_icon="🔍",
    layout="wide"
)

import pydantic_ai
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.groq import GroqModel
import asyncio
from util import load_instruction_from_file
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@st.cache_resource
def initialize_agent():
    try:
        server = MCPServerStdio(
            command='python3',
            args=['/Users/vasstavkumarchava/Desktop/Web Research Agent/server/tools.py'],
        )
        print("MCP server initialized.")
        return Agent(
            model=GroqModel('meta-llama/llama-4-scout-17b-16e-instruct'),
            mcp_servers=[server],
            system_prompt=load_instruction_from_file('systemprompt.txt'),
        )
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return Agent(
            model=GroqModel('meta-llama/llama-4-scout-17b-16e-instruct'),
            system_prompt="You are a helpful assistant knowledgeable."
        )

agent = initialize_agent()

async def process_query(query: str):
    try:
        print("Starting process_query")
        async with agent.run_mcp_servers():
            print("MCP server running")
            result = await agent.run(query)
            print("Agent run completed")

        print("Raw result object:", result)

        if hasattr(result, 'data'):
            print("Data field:", result.output)
            return result.output
        else:
            print("Available attributes:", dir(result))
            return "No recognizable response format returned."

    except Exception as e:
        print(f"Error during query processing: {e}")
        return f"An error occurred: {e}"

def run_asyncio(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            print("Event loop already running, creating task")
            future = asyncio.create_task(coro)
            asyncio.run_coroutine_threadsafe(asyncio.sleep(0.1), loop).result()
            return future
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        print("⚠️ Creating new event loop")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(coro)
        return result



def main():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        if st.button("🔄 Reset Chat"):
            st.session_state.messages = []
            st.rerun()

    st.title("🔍 Web Research Agent")

    # 🔍 Simulate search bar under the title
    prompt = st.chat_input("Ask me anything you'd like to research...")

    # ✅ Display chat only after user starts interaction
    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response = run_asyncio(process_query(prompt))

            if asyncio.isfuture(response) or hasattr(response, "__await__"):
                try:
                    with st.spinner("Thinking..."):
                        if asyncio.isfuture(response):
                            loop = asyncio.get_event_loop()
                            response = asyncio.run_coroutine_threadsafe(
                                asyncio.wait_for(response, timeout=30), 
                                loop
                            ).result()
                        else:
                            response = run_asyncio(response)
                except asyncio.TimeoutError:
                    response = "The response took too long. Please try again."
                except Exception as e:
                    response = f"Error getting response: {str(e)}"

            response_placeholder.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
