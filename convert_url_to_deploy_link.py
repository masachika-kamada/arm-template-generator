import urllib.parse
import argparse


def convert_to_raw_url(github_url):
    if github_url.startswith("https://github.com/"):
        # GitHubのブラウザ表示用URLを「Raw」コンテンツURLに変換
        raw_url = github_url.replace("https://github.com/", "https://raw.githubusercontent.com/")
        raw_url = raw_url.replace("/blob/", "/")
        return raw_url
    return github_url


def generate_deploy_to_azure_link(json_url):
    # URLをエンコード
    encoded_url = urllib.parse.quote(json_url, safe='')

    # 最終的なリンクを生成
    deploy_link = f"https://portal.azure.com/#create/Microsoft.Template/uri/{encoded_url}"

    return deploy_link


def main():
    # コマンドライン引数のパーサーを作成
    parser = argparse.ArgumentParser(description='Generate a "Deploy to Azure" link from a given JSON URL.')
    parser.add_argument('json_url', type=str, help='The URL of the JSON file to be deployed.')

    # 引数を解析
    args = parser.parse_args()

    # GitHubのURLを「Raw」URLに変換
    raw_url = convert_to_raw_url(args.json_url)

    # デプロイリンクを生成
    deploy_link = generate_deploy_to_azure_link(raw_url)

    # 結果を表示
    print(deploy_link)


if __name__ == "__main__":
    main()
