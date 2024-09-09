import os
import re
import subprocess
import sys

from src.llm import generate_bicep_template, fix_bicep_template
from src.urls import convert_to_en_us_url, create_directory_from_url
from src.web_scraper import scrape_web_content

RESOURCE_GROUP = "quickstart"
BICEP_FILE = "azuredeploy.bicep"
PARAMETERS_FILE = "azuredeploy.parameters.json"
MAX_RETRIES = 3


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    url = convert_to_en_us_url(url)
    directory_path = create_directory_from_url(url)
    print(f"Directory path: {directory_path}")

    content = scrape_web_content(url)
    print(content)
    print("=======================================")

    output = generate_bicep_template(content)
    print(output)

    extracted_files = extract_code_blocks(output)
    save_files(directory_path, extracted_files)

    success, message = deploy_bicep(directory_path)
    print(message)

    for i in range(MAX_RETRIES):
        if success:
            break

        print(f"Deployment failed. Retrying... Attempt {i + 1}")

        output = retry_fix_and_deploy(directory_path, output)
        success, message = deploy_bicep(directory_path)
        print(message)


def extract_code_blocks(text):
    code_block_pattern = re.compile(r'```(azuredeploy\.bicep|azuredeploy\.parameters\.json)\n(.*?)\n```', re.DOTALL)
    matches = code_block_pattern.findall(text)

    extracted_files = {}
    for filename, code in matches:
        extracted_files[filename] = code

    return extracted_files


def save_files(directory_path, extracted_files):
    for filename in [BICEP_FILE, PARAMETERS_FILE]:
        save_file(directory_path, filename, extracted_files)


def save_file(directory_path, filename, extracted_files):
    if filename in extracted_files:
        with open(os.path.join(directory_path, filename), "w") as f:
            f.write(extracted_files[filename])
        print(f"{filename} saved successfully.")
    else:
        print(f"{filename} not found in the output.")


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


def retry_fix_and_deploy(directory_path, output):
    with open(os.path.join(directory_path, BICEP_FILE), "r") as f:
        bicep = f.read()
    with open(os.path.join(directory_path, PARAMETERS_FILE), "r") as f:
        parameters_json = f.read()

    output = fix_bicep_template(output, bicep, parameters_json)
    extracted_files = extract_code_blocks(output)
    save_files(directory_path, extracted_files)

    return output


if __name__ == "__main__":
    main()
