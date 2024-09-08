import sys
import os
from src.web_scraper import scrape_web_content
from src.llm import generate_bicep_template
from src.urls import convert_to_en_us_url, create_directory_from_url
import re


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
    result = generate_bicep_template(content)
    print(result)
    extracted_files = extract_code_blocks(result)

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


if __name__ == "__main__":
    main()
