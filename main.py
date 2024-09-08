import os
import re
import subprocess
import sys

from src.llm import generate_bicep_template, fix_bicep_template
from src.urls import convert_to_en_us_url, create_directory_from_url
from src.web_scraper import scrape_web_content


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

    save_file(directory_path, "azuredeploy.bicep", extracted_files)
    save_file(directory_path, "azuredeploy.parameters.json", extracted_files)

    for i in range(3):
        result, output = deploy_bicep(
            "quickstart",
            os.path.join(directory_path, "azuredeploy.bicep"),
            os.path.join(directory_path, "azuredeploy.parameters.json")
        )
        if result:
            break
        print(f"Deployment failed. Retrying... Attempt {i + 1}")
        print(output)

        with open(os.path.join(directory_path, "azuredeploy.bicep"), "r") as f:
            bicep = f.read()
        with open(os.path.join(directory_path, "azuredeploy.parameters.json"), "r") as f:
            parameters_json = f.read()
        output = fix_bicep_template(output, bicep, parameters_json)
        extracted_files = extract_code_blocks(output)

        save_file(directory_path, "azuredeploy.bicep", extracted_files)
        save_file(directory_path, "azuredeploy.parameters.json", extracted_files)


def extract_code_blocks(text):
    code_block_pattern = re.compile(r'```(azuredeploy\.bicep|azuredeploy\.parameters\.json)\n(.*?)\n```', re.DOTALL)
    matches = code_block_pattern.findall(text)

    extracted_files = {}
    for filename, code in matches:
        extracted_files[filename] = code

    return extracted_files


def save_file(directory_path, filename, extracted_files):
    if filename in extracted_files:
        with open(os.path.join(directory_path, filename), "w") as f:
            f.write(extracted_files[filename])
        print(f"{filename} saved successfully.")
    else:
        print(f"{filename} not found in the output.")


def deploy_bicep(resource_group, template_file, parameters_file):
    command = [
        "az",
        "deployment",
        "group",
        "create",
        "--resource-group",
        resource_group,
        "--template-file",
        template_file,
        "--parameters",
        parameters_file,
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, shell=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


if __name__ == "__main__":
    main()
