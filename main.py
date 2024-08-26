import sys
import json
from src.fetch_content import fetch_content
from src.generate_template import generate_template
import re


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    content = fetch_content(url)
    print(content)
    print("=======================================")
    result = generate_template(content)
    template = json.loads(extract_code_blocks(result))

    with open('output.json', 'w') as f:
        json.dump(template, f, indent=4)

    print(template)


def extract_code_blocks(text):
    # 正規表現で```jsonまたは```で始まる行を見つける
    code_block_pattern = re.compile(r'```(?:json)?\n(.*?)\n```', re.DOTALL)
    matches = code_block_pattern.findall(text)

    # 抽出されたコードブロックを結合して返す
    return "\n".join(matches)


if __name__ == "__main__":
    main()
