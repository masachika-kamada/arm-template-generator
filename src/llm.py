from pathlib import Path

from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI

load_dotenv(Path(__file__).parent / "../.env")

with open(Path(__file__).parent / "../prompts/main.txt", "r") as f:
    system_prompt = f.read()
with open(Path(__file__).parent / "../prompts/fix.txt", "r") as f:
    fix_prompt = f.read()


def generate_bicep_template(prompt):
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt),
    ]
    llm = AzureChatOpenAI(azure_deployment="gpt-4o", temperature=0)
    res = llm.invoke(messages)
    return res.content


def fix_bicep_template(error_message, bicep, parameters_json):
    messages = [
        SystemMessage(content="You are the best engineer in the world. Please answer the user's questions accurately."),
        HumanMessage(content=fix_prompt
                     .replace("ERROR_MESSAGE", error_message)
                     .replace("BICEP", bicep)
                     .replace("PARAMETERS_JSON", parameters_json)),
    ]
    llm = AzureChatOpenAI(azure_deployment="gpt-4o", temperature=0)
    res = llm.invoke(messages)
    return res.content
