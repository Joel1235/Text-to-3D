import requests
import os
import json

from dotenv import load_dotenv; load_dotenv()

prompt = f"""
    Validate if the input is a valid request for a 3D object. A valid input should specify a clear, singular object (e.g., "I want a 3D model of a chair"). If valid, respond with "true". If not, respond with "false". Do not output anything else. 
    Input: 
    """

def validate_user_input(user_input: str) -> bool:
    llm_prompt = prompt + user_input
    api_key = os.getenv("API_KEY")
    llm_url = os.getenv("LLM_URL")

    payload = {
        "messages": [
            {"role": "system", "content": "You are an assistant."},
            {"role": "user", "content": llm_prompt}
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
    print(llm_response)
    valid_flag = llm_response.lower() == "true"
    return valid_flag
