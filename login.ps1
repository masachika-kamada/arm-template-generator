# .envファイルのパスを指定
$envFilePath = ".env"

# .envファイルを読み込む
$envContent = Get-Content $envFilePath

# 各行を処理して環境変数を設定
foreach ($line in $envContent) {
    $line = $line.Trim()
    if ($line -and -not $line.StartsWith("#")) {
        $parts = $line -split "=", 2
        if ($parts.Length -eq 2) {
            $name = $parts[0].Trim()
            $value = $parts[1].Trim()
            [System.Environment]::SetEnvironmentVariable($name, $value, [System.EnvironmentVariableTarget]::Process)
        }
    }
}

# 環境変数からテナントIDを取得
$tenantId = [System.Environment]::GetEnvironmentVariable('AZURE_TENANT_ID', [System.EnvironmentVariableTarget]::Process)

# az login コマンドを実行
az login --tenant $tenantId
