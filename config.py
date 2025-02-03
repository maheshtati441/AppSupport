import os

# Azure OpenAI Configuration
ENDPOINT_URL = os.getenv("ENDPOINT_URL", "https://mahes-m6n9mtgc-eastus2.openai.azure.com/")
DEPLOYMENT = os.getenv("mahes-m6n9mtgc-eastus2", "gpt-4")
SUBSCRIPTION_KEY = os.getenv("AZURE_OPENAI_API_KEY",
                                 "1U5eSvw1tKJexQqkBHRNjNmx2YtccCt1R9clqFMryo1eWfd8okaiJQQJ99BBACHYHv6XJ3w3AAAAACOGswdF")
