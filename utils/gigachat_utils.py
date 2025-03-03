import os
from dotenv import load_dotenv
import requests
import json
import logging

load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Authentication parameters
GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")  # Client ID and Client Secret in base64 format
GIGACHAT_AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"  # URL to get the token
GIGACHAT_API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"  # API URL
GIGACHAT_MODEL = "GigaChat"  # Model name

def get_gigachat_token():
    """Gets the access token for the GigaChat API."""
    if not GIGACHAT_CREDENTIALS:
        logging.error("Gigachat credentials not found. Set the GIGACHAT_CREDENTIALS environment variable.")
        return None

    headers = {
        'Authorization': f'Basic {GIGACHAT_CREDENTIALS}',
        'RqUID': '6f0b1291-c7f3-43c6-bb2e-9f3efb2dc98e',  # Unique request identifier
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'scope': 'GIGACHAT_API_PERS'
    }

    try:
        response = requests.post(GIGACHAT_AUTH_URL, headers=headers, data=data, verify=False)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get('access_token')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting token: {e}")
        return None

def generate_comic_scenario(text, model=GIGACHAT_MODEL):
    """Uses GigaChat to create a comic scenario based on the text."""
    access_token = get_gigachat_token()
    if not access_token:
        logging.error("Failed to get access token.")
        return None

    prompt = f"Turn this text into a comic scenario with dialogues and descriptions: {text}\n\n" \
             f"The scenario should be short, humorous, and suitable for visualization in a comic. " \
             f"Each scene should be clearly separated. The script should explicitly indicate characters and their dialogues. " \
             f"Generate only 1 scene with 4 frames."  # MODIFIED LINE

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,  # Parameter to control creativity
        "max_tokens": 1024   # Maximum number of tokens in the response
    }

    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.post(GIGACHAT_API_URL, headers=headers, json=payload, verify=False)
        response.raise_for_status()

        response_json = response.json()
        generated_text = response_json["choices"][0]["message"]["content"]
        logging.info(f"Generated text: {generated_text}")
        return generated_text.strip()

    except requests.exceptions.HTTPError as e:
        logging.error(f"Error requesting the GIGACHAT API: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        logging.exception(f"General error: {e}")
        return None