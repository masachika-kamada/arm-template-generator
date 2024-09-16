import os

from dotenv import load_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv("../.env")


def initialize_vector_store(index_name, embedding_function):
    return AzureSearch(
        azure_search_endpoint=os.environ.get("AZURE_SEARCH_ENDPOINT"),
        azure_search_key=os.environ.get("AZURE_SEARCH_ADMIN_KEY"),
        index_name=index_name,
        embedding_function=embedding_function
    )


def main():
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment="text-embedding-3-large",
        openai_api_version="2023-05-15"
    )
    vector_store = initialize_vector_store(
        index_name="quickstarts",
        embedding_function=embeddings.embed_query
    )
    # vector search
    result_docs = vector_store.similarity_search(
        query="Virtual Machine Linux Deployment",
        k=3,
        search_type="hybrid"
    )
    # print the results
    for doc in result_docs:
        print(doc.json(indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
