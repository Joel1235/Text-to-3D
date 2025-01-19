import requests
import os
import json

from dotenv import load_dotenv; load_dotenv()


def llm_req(prompt: str):
    api_key = os.getenv("API_KEY")
    llm_url = os.getenv("LLM_URL")

    payload = {
        "messages": [
            {"role": "system", "content": "You are an assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }

    llm_headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    response = requests.post(llm_url, json=payload, headers=llm_headers)
    llm_response = response.json()["choices"][0]["message"]["content"]
    print("\n LLM RESPONSE: \n" + llm_response + "\n for using this prompt: \n" + prompt)
    return llm_response
