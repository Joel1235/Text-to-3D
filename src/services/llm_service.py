import requests
import os
import json
import logging

from dotenv import load_dotenv; load_dotenv()


#simple service for communication with LLM
def llm_req(prompt: str, system_prompt: str):
    api_key = os.getenv("API_KEY")
    llm_url = os.getenv("LLM_URL")

    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
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
    logging.info("LLM Response received: %s", llm_response)
    return llm_response
