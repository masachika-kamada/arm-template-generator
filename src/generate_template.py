from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / "../.env")


def generate_template(prompt):
    messages = [
        SystemMessage(content="Generate an ARM template based on the Azure Quickstart document provided by the user.  When outputting the JSON, enclose it in a code block using triple backticks."),
        HumanMessage(content=prompt),
    ]
    llm = AzureChatOpenAI(azure_deployment="gpt-4o", temperature=0)
    res = llm.invoke(messages)
    return res.content
