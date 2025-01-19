# DDEAI Project Setup
Project for Data-Driven Engineering. Implementing an AI-assistant for creating `stl`-files

## Configuration
Create a `.env` file and add the following values:

```env
API_KEY= <your_llms_api_key_here>
LLM_URL= <your-llms-api-url>
MESHY_API_KEY= <your_meshy_api_key_here>
MESHY_URL= <your-meshy-api-url>
``` 

## Installation
First, install the required Python packages:
````python
pip install -r requirements.txt
````

Once the requirements are installed, you can start the application by running the main script:
````python
python src/main.py
````

