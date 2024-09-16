from pathlib import Path
import re

from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_openai import AzureChatOpenAI
from src.web_scraper import scrape_web_content


class BicepDeployer:
    def __init__(self):
        load_dotenv(Path(__file__).parent / "../.env")

        with open(Path(__file__).parent / "../prompts/main.txt", "r") as f:
            self.system_prompt = f.read()
        self.messages = [
            SystemMessage(content=self.system_prompt)
        ]
        with open(Path(__file__).parent / "../prompts/fix.txt", "r") as f:
            self.fix_prompt = f.read()

        # https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api/172683
        self.llm = AzureChatOpenAI(azure_deployment="gpt-4o", temperature=0.2, top_p=0.1)

    def generate_bicep_template(self, mslearn_content):
        self.messages.append(HumanMessage(content=mslearn_content))
        res = self.llm.invoke(self.messages)
        self.messages.append(AIMessage(content=res.content))
        return res.content

    def fix_bicep_template(self, error_message):
        # If the error_message contains a URL, retrieve the content of that page and add it to the error_message.
        urls = re.findall(r"https?://[^\s]+", error_message)
        for url in urls:
            content = scrape_web_content(url)
            error_message += f"\n\n```{url}\n{content}\n```"

        self.messages.append(HumanMessage(content=self.fix_prompt.replace("ERROR_MESSAGE", error_message)))
        res = self.llm.invoke(self.messages)
        self.messages.append(AIMessage(content=res.content))
        return res.content
