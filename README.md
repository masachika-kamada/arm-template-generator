# ARM Template Generator

## Overview

The ARM Template Generator is a tool designed to simplify the creation and deployment of Azure Resource Manager (ARM) templates. This tool allows you to generate ARM templates from Azure Quickstart documents, create deploy links, and deploy the templates to your Azure environment.

## Prerequisites

* Python 3.10
* Azure CLI
* Git

## Usage

### Setup

1. Create a virtual environment and activate it:

    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use `activate.ps1`
    ```
2. Install the required packages:

    ```
    pip install -r requirements.txt
    ```

### Generate ARM Template

1. Create a `.env` file based on `.env.sample.`

2. Run the script to generate the ARM template:

    ```
    python main.py https://learn.microsoft.com/azure/virtual-machines/linux/quick-create-portal?tabs=ubuntu
    ```

### Create Deploy Link

1. Commit and push the generated ARM template to your GitHub repository.

2. Run the script to convert the GitHub URL to a deploy link:

    ```
    python convert_url_to_deploy_link.py [GitHub ARM template URL]
    ```

### Deploy

1. Edit the .env file and define the `AZURE_TENANT_ID`.

2. Log in to Azure:

    ```
    ./login.ps1
    ```

3. Deploy the ARM template:

    ```
    az deployment group create --resource-group sample --template-file output.json
    ```
