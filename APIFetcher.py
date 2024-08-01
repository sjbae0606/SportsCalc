import requests
import yaml
import logging

# Load configuration
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

logging.basicConfig(filename=config['logging']['file'], level=config['logging']['level'])

def fetch_sports_data():
    api_key = config['api']['key']
    api_url = config['api']['url']
    response = requests.get(f"{api_url}?apiKey={api_key}")

    if response.status_code != 200:
        logging.error(f"Failed to retrieve data: {response.status_code}")
        return []

    data = response.json()
    logging.info("Successfully fetched sports data from API")
    return data
