import time
from openai import AzureOpenAI
from logging_setup import logger
from config import ENDPOINT_URL, DEPLOYMENT, SUBSCRIPTION_KEY
import streamlit as st


# Initialize Azure OpenAI Service client
client = AzureOpenAI(
    azure_endpoint=ENDPOINT_URL,
    api_key=SUBSCRIPTION_KEY,
    api_version="2024-05-01-preview",
)

def search_similar_issues(df, issue_description):
    """Search for similar issues in the dataset."""
    try:
        if 'Issue' not in df.columns or 'Resolution' not in df.columns:
            logger.warning("Uploaded file missing required columns.")
            st.error("Uploaded file must contain 'Issue' and 'Resolution' columns.")
            return []

        # Filter only closed issues
        closed_issues = df[df['Status'].str.lower() == 'closed']

        #results = df[df['Issue'].str.contains(issue_description, case=False, na=False)].to_dict(orient='records')
        results = closed_issues[closed_issues['Issue'].str.contains(issue_description, case=False, na=False)].to_dict(orient='records')
        logger.info(f"Found {len(results)} similar issues.")
        return results
    except Exception as e:
        logger.error(f"Error searching for similar issues: {e}")
        return []


def generate_ai_response(issue_description):
    """Generate an AI response for troubleshooting the issue."""
    chat_prompt = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": f"""As an experienced application support engineer, provide a detailed troubleshooting guide:
                                    Issue: {issue_description}
                                    Steps to troubleshoot and resolve the issue should include:
                                        - Possible root causes
                                        - Step-by-step diagnostic approach
                                        - Recommended solutions
                                        - Any relevant commands, scripts, or tools to use
                                        - Preventative measures to avoid recurrence"""
                }
            ]
        }
    ]
    messages = chat_prompt
    try:
        start_time = time.time()
        completion = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=messages,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=True)
        elapsed_time = time.time() - start_time
        logger.info(f"AI response generated in {elapsed_time:.2f} seconds.")
        return completion
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return "Error generating AI response. Please try again."
