az group create --name sample --location eastus

az deployment group create --resource-group sample --template-file azuredeploy.json
