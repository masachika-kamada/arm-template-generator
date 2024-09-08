import sys
from src.fetch_content import fetch_content
from src.generate_template import generate_template
from src.urls import *
import re


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    url = convert_to_english_url(url)
    directory_path = create_directory_from_url(url)
    print(f"directory_path: {directory_path}")
    content = fetch_content(url)
    print(content)
    print("=======================================")
    result = generate_template(content)
    print(result)
    extracted_files = extract_code_blocks(result)

    # azuredeploy.bicepの保存
    if 'azuredeploy.bicep' in extracted_files:
        with open(os.path.join(directory_path, 'azuredeploy.bicep'), 'w') as f:
            f.write(extracted_files['azuredeploy.bicep'])
        print("azuredeploy.bicep saved successfully.")
    else:
        print("azuredeploy.bicep not found in the output.")

    # azuredeploy.parameters.jsonの保存
    if 'azuredeploy.parameters.json' in extracted_files:
        with open(os.path.join(directory_path, 'azuredeploy.parameters.json'), 'w') as f:
            f.write(extracted_files['azuredeploy.parameters.json'])
        print("azuredeploy.parameters.json saved successfully.")
    else:
        print("azuredeploy.parameters.json not found in the output.")


def extract_code_blocks(text):
    # 正規表現で```azuredeploy.bicep```または```azuredeploy.parameters.json```で始まる行を見つける
    code_block_pattern = re.compile(r'```(azuredeploy\.bicep|azuredeploy\.parameters\.json)\n(.*?)\n```', re.DOTALL)
    matches = code_block_pattern.findall(text)

    # 抽出されたコードブロックを辞書に格納して返す
    extracted_files = {}
    for match in matches:
        filename, code = match
        extracted_files[filename] = code

    return extracted_files


if __name__ == "__main__":
    main()
