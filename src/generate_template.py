from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / "../.env")
with open(Path(__file__).parent / "../prompts/system_prompt.txt", "r") as f:
    system_prompt = f.read()


def generate_template(prompt):
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt),
    ]
    llm = AzureChatOpenAI(azure_deployment="gpt-4o", temperature=0)
    res = llm.invoke(messages)
    return res.content
