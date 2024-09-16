import os
import re
import subprocess
import sys
import json

from src.llm import BicepDeployer
from src.urls import create_directory_from_url
from src.web_scraper import scrape_web_content
from src.file_io import save_files

RESOURCE_GROUP = "quickstart"
BICEP_FILE = "azuredeploy.bicep"
PARAMETERS_FILE = "azuredeploy.parameters.json"
MAX_RETRIES = 3


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    directory_path = create_directory_from_url(url)
    print(f"Directory path: {directory_path}")

    content = scrape_web_content(url)
    print(content)
    print("==========")

    deployer = BicepDeployer()
    success = False
    for i in range(1 + MAX_RETRIES):
        if success:
            break

        if i == 0:
            output = deployer.generate_bicep_template(content)
        else:
            print(f"==========\nRetrying... Attempt {i}")
            output = deployer.fix_bicep_template(message)

        extracted_files = extract_code_blocks(output)
        save_files(directory_path, [BICEP_FILE, PARAMETERS_FILE], extracted_files)

        success, message = deploy_bicep(directory_path)
        print(message)

    messages_dict = [{"type": message.type, "content": message.content} for message in deployer.messages]

    # Save messages to a JSON file
    with open("messages.json", "w") as f:
        json.dump(messages_dict, f, indent=4)


def extract_code_blocks(text):
    code_block_pattern = re.compile(r'```(azuredeploy\.bicep|azuredeploy\.parameters\.json)\n(.*?)\n```', re.DOTALL)
    matches = code_block_pattern.findall(text)

    extracted_files = {}
    for filename, code in matches:
        # There is a possibility that file names may be duplicated in the process of creating deliverables, but they will eventually be overwritten.
        extracted_files[filename] = code

    return extracted_files


def deploy_bicep(directory_path):
    command = [
        "az",
        "deployment",
        "group",
        "create",
        "--resource-group",
        RESOURCE_GROUP,
        "--template-file",
        os.path.join(directory_path, BICEP_FILE),
        "--parameters",
        os.path.join(directory_path, PARAMETERS_FILE),
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, shell=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


if __name__ == "__main__":
    main()
