import re
import os
from urllib.parse import urlparse, unquote


def convert_to_english_url(url):
    # 正規表現でlearn.microsoft.comの直後の任意の文字列を検出し、'en-us'に置き換える
    new_url = re.sub(r'(https://learn\.microsoft\.com/)([^/]+/)', r'\1en-us/', url)
    return new_url


def create_directory_from_url(url):
    print(url)
    # URLを解析
    parsed_url = urlparse(url)
    path = parsed_url.path
    query = parsed_url.query

    # パス部分を階層ごとに分割
    path_parts = path.strip('/').split('/')

    # 'en-us'と'azure'を除外
    if path_parts[0] == 'en-us':
        path_parts = path_parts[1:]
    if path_parts[0] == 'azure':
        path_parts = path_parts[1:]

    # クエリパラメータを含む最後の部分を特別に処理
    if query:
        query = unquote(query)
        path_parts[-1] = f"{path_parts[-1]}_{query}"

    # 各階層のディレクトリ名を適切に処理
    sanitized_parts = [re.sub(r'[<>:"/\\|?&]', '_', part) for part in path_parts]

    # ディレクトリパスを作成
    directory_path = os.path.join('deploy', *sanitized_parts)

    # ディレクトリを作成（存在しない場合のみ）
    os.makedirs(directory_path, exist_ok=True)
    return directory_path
