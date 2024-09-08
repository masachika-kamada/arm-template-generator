from pathlib import Path

from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI

load_dotenv(Path(__file__).parent / "../.env")
with open(Path(__file__).parent / "../prompts/system_prompt.txt", "r") as f:
    system_prompt = f.read()


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
        HumanMessage(content="When trying to deploy using `az deployment group create --resource-group quickstart --template-file azuredeploy.bicep --parameters azuredeploy.parameters.json`, the following error occurred. Please identify the cause and explain how to fix the files.\nOutput format: Enclose the output Bicep file and parameters.json file in code blocks like:\n```azuredeploy.bicep\n<content>\n```\n```azuredeploy.parameters.json\n<content>\n```\n\nError message:\n" + error_message + "\n\n```azuredeploy.bicep\n" + bicep + "\n```\n\n```azuredeploy.parameters.json\n" + parameters_json + "\n```"),
    ]
    llm = AzureChatOpenAI(azure_deployment="gpt-4o", temperature=0)
    res = llm.invoke(messages)
    return res.content
