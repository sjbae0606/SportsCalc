import requests
from bs4 import BeautifulSoup
import yaml
import logging

# Load configuration
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

logging.basicConfig(filename=config['logging']['file'], level=config['logging']['level'])

def scrape_betting_odds(url):
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve data: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    odds_data = []
    for item in soup.find_all('div', class_='odds-item'):
        event_name = item.find('span', class_='event-name').text.strip()
        odds_value = item.find('span', class_='odds-value').text.strip()
        odds_data.append({'event': event_name, 'odds': odds_value})

    logging.info("Successfully scraped betting odds data")
    return odds_data
