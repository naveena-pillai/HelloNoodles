import requests
import time
import csv
from datetime import datetime
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import base64

# Kalshi API credentials
API_KEY_ID = 'ee9165d8-5173-4c0f-a764-006598891621'
PRIVATE_KEY_PATH = 'kalshi.txt'
BASE_URL = 'https://api.elections.kalshi.com/trade-api/v2'

def load_private_key(path):
    with open(path, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

PRIVATE_KEY = load_private_key(PRIVATE_KEY_PATH)

def sign_request(timestamp: str, method: str, request_path: str) -> str:
    message = f"{timestamp}{method.upper()}{request_path}".encode('utf-8')
    signature = PRIVATE_KEY.sign(
        message,
        padding=padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        algorithm=hashes.SHA256(),
    )
    return base64.b64encode(signature).decode('utf-8')

def get_open_events() -> list:
    path = '/events?status=open&limit=100'
    all_events = []
    cursor = None

    while True:
        timestamp = str(int(datetime.utcnow().timestamp() * 1000))
        full_path = path + (f"&cursor={cursor}" if cursor else "")
        signature = sign_request(timestamp, 'GET', full_path)

        headers = {
            'KALSHI-ACCESS-KEY': API_KEY_ID,
            'KALSHI-ACCESS-TIMESTAMP': timestamp,
            'KALSHI-ACCESS-SIGNATURE': signature,
            'Accept': 'application/json'
        }

        url = BASE_URL + full_path
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        all_events.extend(data.get('events', []))

        cursor = data.get('cursor')
        if not cursor:
            break

    return all_events

def get_event_markets(event_ticker: str) -> list:
    path = f'/events/{event_ticker}'
    timestamp = str(int(datetime.utcnow().timestamp() * 1000))
    signature = sign_request(timestamp, 'GET', path)

    headers = {
        'KALSHI-ACCESS-KEY': API_KEY_ID,
        'KALSHI-ACCESS-TIMESTAMP': timestamp,
        'KALSHI-ACCESS-SIGNATURE': signature,
        'Accept': 'application/json'
    }

    url = BASE_URL + path
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json().get('markets', [])

def get_market_prices(market_ticker: str) -> list:
    path = f'/markets/{market_ticker}/history?limit=100'
    timestamp = str(int(datetime.utcnow().timestamp() * 1000))
    signature = sign_request(timestamp, 'GET', path)
    
    headers = {
        'KALSHI-ACCESS-KEY': API_KEY_ID,
        'KALSHI-ACCESS-TIMESTAMP': timestamp,
        'KALSHI-ACCESS-SIGNATURE': signature,
        'Accept': 'application/json'
    }

    url = BASE_URL + path
    resp = requests.get(url, headers=headers)
    if resp.status_code == 404:
        return []  # Some tickers may not have prices
    resp.raise_for_status()
    return resp.json().get('prices', [])

def scrape_sports_markets(output_csv: str = 'kalshi_sports_prices.csv') -> None:
    events = get_open_events()
    sports_events = [e for e in events if e.get('category', '').lower() == 'sports']#[:10]  # Limit to 10 for testing

    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'event_ticker', 'yes_sub_title','market_ticker', 'yes_bid', 'yes_ask', 'no_bid', 'no_ask', 'last_price'])

        for ev in sports_events:
            event_ticker = ev.get('event_ticker')
            if "MLB" in event_ticker:
                if not event_ticker.startswith('KXMLBWORLD'):
                    try:
                        markets = get_event_markets(event_ticker)
                        for market in markets:
                            ticker = market.get('ticker')
                            if not ticker:
                                continue
        
                            # Directly extract prices from market object
                            yes_sub_title = market.get('yes_sub_title')
                            yes_bid = market.get('yes_bid')
                            yes_ask = market.get('yes_ask')
                            no_bid = market.get('no_bid')
                            no_ask = market.get('no_ask')
                            last_price = market.get('last_price')
                            timestamp = datetime.utcnow().isoformat()
        
                            writer.writerow([timestamp, event_ticker, yes_sub_title, ticker, yes_bid, yes_ask, no_bid, no_ask, last_price])
                            time.sleep(0.1)
                    except Exception as e:
                        print(f"[ERROR] Failed to get markets for {event_ticker}: {e}")

if __name__ == '__main__':
    scrape_sports_markets()
    print('Sports scraping complete. CSV saved.')