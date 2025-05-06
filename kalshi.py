# # import requests
# # import time
# # import csv
# # from datetime import datetime
# # from cryptography.hazmat.primitives import serialization, hashes
# # from cryptography.hazmat.primitives.asymmetric import padding
# # from cryptography.hazmat.backends import default_backend
# # import base64

# # # Your Kalshi API credentials
# # API_KEY_ID = '2dc1eefe-5e3c-447b-9536-8fb59bbee5b7'
# # PRIVATE_KEY_PATH = 'naveena.txt'

# # # Use the Kalshi sandbox environment for testing
# # BASE_URL = 'https://api.elections.kalshi.com/trade-api/v2'

# # # Load your RSA private key for signing
# # def load_private_key(path):
# #     with open(path, 'rb') as f:
# #         return serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

# # PRIVATE_KEY = load_private_key(PRIVATE_KEY_PATH)

# # def sign_request(timestamp: str, method: str, request_path: str) -> str:
# #     message = f"{timestamp}{method.upper()}{request_path}".encode('utf-8')
# #     signature = PRIVATE_KEY.sign(
# #         message,
# #         padding=padding.PSS(
# #             mgf=padding.MGF1(hashes.SHA256()),
# #             salt_length=padding.PSS.MAX_LENGTH,
# #         ),
# #         algorithm=hashes.SHA256(),
# #     )
# #     return base64.b64encode(signature).decode('utf-8')

# # def get_open_events() -> list:
# #     path = '/events?status=open&limit=100'
# #     all_events = []
# #     cursor = None

# #     while True:
# #         timestamp = str(int(datetime.utcnow().timestamp() * 1000))
# #         full_path = path + (f"&cursor={cursor}" if cursor else "")
# #         signature = sign_request(timestamp, 'GET', full_path)

# #         headers = {
# #             'KALSHI-ACCESS-KEY': API_KEY_ID,
# #             'KALSHI-ACCESS-TIMESTAMP': timestamp,
# #             'KALSHI-ACCESS-SIGNATURE': signature,
# #             'Accept': 'application/json'
# #         }

# #         url = BASE_URL + full_path
# #         resp = requests.get(url, headers=headers)
# #         resp.raise_for_status()
# #         data = resp.json()
# #         all_events.extend(data.get('events', []))

# #         cursor = data.get('cursor')
# #         if not cursor:
# #             break

# #     return all_events

# # def get_mlb_events() -> list:
# #     events = get_open_events()
# #     mlb = []
# #     for e in events:
# #         cat = e.get('category', '') or ''
# #         title = e.get('title', '') or ''
# #         print(f"[DEBUG] Category: {cat} | Title: {title}")
# #         if 'sports' in cat.lower() and 'vs' in title.lower():
# #             mlb.append(e)
# #     return mlb

# # def get_market_prices(market_ticker: str) -> list:
# #     """
# #     Fetch historical prices for a given market ticker.
# #     """
# #     path = f'/markets/{market_ticker}/history?limit=100'
# #     timestamp = str(int(datetime.utcnow().timestamp() * 1000))
# #     signature = sign_request(timestamp, 'GET', path)
# #     headers = {
# #         'KALSHI-ACCESS-KEY': API_KEY_ID,
# #         'KALSHI-ACCESS-TIMESTAMP': timestamp,
# #         'KALSHI-ACCESS-SIGNATURE': signature,
# #         'Accept': 'application/json'
# #     }

# #     url = BASE_URL + path
# #     resp = requests.get(url, headers=headers)
# #     resp.raise_for_status()
# #     return resp.json().get('prices', [])

# # def scrape_mlb_markets(output_csv: str = 'kalshi_mlb_prices.csv') -> None:
# #     mlb_events = get_mlb_events()
# #     with open(output_csv, 'w', newline='') as f:
# #         writer = csv.writer(f)
# #         writer.writerow(['timestamp', 'event_ticker', 'market_ticker', 'yes_price', 'no_price'])

# #         for ev in mlb_events:
# #             event_ticker = ev.get('event_ticker')
# #             for market in ev.get('markets', []):
# #                 ticker = market.get('ticker')
# #                 prices = get_market_prices(ticker)
# #                 if prices:
# #                     latest = prices[-1]
# #                     ts = latest.get('ts')
# #                     yes = next((p['price'] for p in prices if p['side'] == 'YES'), None)
# #                     no = next((p['price'] for p in prices if p['side'] == 'NO'), None)
# #                 else:
# #                     ts = yes = no = None
# #                 writer.writerow([ts, event_ticker, ticker, yes, no])
# #                 time.sleep(0.2)

# # if __name__ == '__main__':
# #     scrape_mlb_markets()
# #     print('MLB scraping complete. CSV saved.')

# import requests
# import time
# import csv
# from datetime import datetime
# from cryptography.hazmat.primitives import serialization, hashes
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.backends import default_backend
# import base64

# API_KEY_ID = '2dc1eefe-5e3c-447b-9536-8fb59bbee5b7'
# PRIVATE_KEY_PATH = 'naveena.txt'
# BASE_URL = 'https://api.elections.kalshi.com/trade-api/v2'

# def load_private_key(path):
#     with open(path, 'rb') as f:
#         return serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

# PRIVATE_KEY = load_private_key(PRIVATE_KEY_PATH)

# def sign_request(timestamp: str, method: str, request_path: str) -> str:
#     message = f"{timestamp}{method.upper()}{request_path}".encode('utf-8')
#     signature = PRIVATE_KEY.sign(
#         message,
#         padding=padding.PSS(
#             mgf=padding.MGF1(hashes.SHA256()),
#             salt_length=padding.PSS.MAX_LENGTH,
#         ),
#         algorithm=hashes.SHA256(),
#     )
#     return base64.b64encode(signature).decode('utf-8')

# def get_open_events() -> list:
#     path = '/markets?status=open&limit=100'
#     all_events = []
#     cursor = None

#     while True:
#         timestamp = str(int(datetime.utcnow().timestamp() * 1000))
#         full_path = path + (f"&cursor={cursor}" if cursor else "")
#         signature = sign_request(timestamp, 'GET', full_path)

#         headers = {
#             'KALSHI-ACCESS-KEY': API_KEY_ID,
#             'KALSHI-ACCESS-TIMESTAMP': timestamp,
#             'KALSHI-ACCESS-SIGNATURE': signature,
#             'Accept': 'application/json'
#         }

#         url = BASE_URL + full_path
#         resp = requests.get(url, headers=headers)
#         resp.raise_for_status()
#         data = resp.json()
#         all_events.extend(data.get('events', []))

#         cursor = data.get('cursor')
#         if not cursor:
#             break

#     return all_events

# def get_sports_events() -> list:
#     events = get_open_events()
#     sports = []
#     for e in events:
#         cat = e.get('category', '') or ''
#         title = e.get('title', '') or ''
#         if 'sports' in cat.lower():
#             # print(f"[DEBUG] Category: {cat} | Title: {title}")
#             sports.append(e)
#     return sports

# def get_market_prices(market_ticker: str) -> list:
#     path = f'/markets/{market_ticker}/history?limit=100'
#     timestamp = str(int(datetime.utcnow().timestamp() * 1000))
#     signature = sign_request(timestamp, 'GET', path)
#     headers = {
#         'KALSHI-ACCESS-KEY': API_KEY_ID,
#         'KALSHI-ACCESS-TIMESTAMP': timestamp,
#         'KALSHI-ACCESS-SIGNATURE': signature,
#         'Accept': 'application/json'
#     }

#     url = BASE_URL + path
#     resp = requests.get(url, headers=headers)
#     resp.raise_for_status()
#     return resp.json().get('prices', [])

# def get_event_markets(event_ticker: str) -> list:
#     path = f'/events/{event_ticker}'
#     timestamp = str(int(datetime.utcnow().timestamp() * 1000))
#     signature = sign_request(timestamp, 'GET', path)

#     headers = {
#         'KALSHI-ACCESS-KEY': API_KEY_ID,
#         'KALSHI-ACCESS-TIMESTAMP': timestamp,
#         'KALSHI-ACCESS-SIGNATURE': signature,
#         'Accept': 'application/json'
#     }

#     url = BASE_URL + path
#     resp = requests.get(url, headers=headers)
#     resp.raise_for_status()
#     return resp.json().get('markets', [])

# def scrape_sports_markets(output_csv: str = 'kalshi_sports_prices.csv') -> None:
#     sports_events = get_sports_events()
#     print(sports_events)
#     with open(output_csv, 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['timestamp', 'event_ticker', 'market_ticker', 'yes_price', 'no_price'])

#         for ev in sports_events:
#             event_ticker = ev.get('event_ticker')
#             markets = get_event_markets(event_ticker)
#             for market in markets:
#                 try:
#                     prices = get_market_prices(event_ticker)
#                 except requests.exceptions.HTTPError as e:
#                     print(f"[WARNING] Could not fetch prices for {event_ticker}: {e}")
#                     continue

#             # for market in markets:
#             #     ticker = market.get('ticker')
#             #     prices = get_market_prices(ticker)
#             #     if prices:
#             #         latest = prices[-1]
#             #         ts = latest.get('ts')
#             #         yes = next((p['price'] for p in prices if p['side'] == 'YES'), None)
#             #         no = next((p['price'] for p in prices if p['side'] == 'NO'), None)
#             #     else:
#             #         ts = yes = no = None
#             #     writer.writerow([ts, event_ticker, ticker, yes, no])
#             #     time.sleep(0.2)

# if __name__ == '__main__':
#     scrape_sports_markets()
#     print('Sports scraping complete. CSV saved.')

import requests
import time
import csv
from datetime import datetime
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import base64

# Kalshi API credentials
API_KEY_ID = '2dc1eefe-5e3c-447b-9536-8fb59bbee5b7'
PRIVATE_KEY_PATH = 'naveena.txt'
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
    sports_events = [e for e in events if e.get('category', '').lower() == 'sports'][:10]  # Limit to 10

    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'event_ticker', 'market_ticker', 'yes_price', 'no_price'])

        for ev in sports_events:
            event_ticker = ev.get('event_ticker')
            try:
                markets = get_event_markets(event_ticker)
            except Exception as e:
                print(f"[ERROR] Failed to get markets for {event_ticker}: {e}")
                continue

            for market in markets:
                ticker = market.get('ticker')
                if not ticker:
                    continue
                try:
                    prices = get_market_prices(ticker)
                    yes_price = next((p['price'] for p in reversed(prices) if p['side'] == 'YES'), None)
                    no_price = next((p['price'] for p in reversed(prices) if p['side'] == 'NO'), None)
                    timestamp = prices[-1].get('ts') if prices else None
                    writer.writerow([timestamp, event_ticker, ticker, yes_price, no_price])
                    time.sleep(0.2)
                except Exception as e:
                    print(f"[WARNING] Could not fetch prices for {ticker}: {e}")

if __name__ == '__main__':
    scrape_sports_markets()
    print('Sports scraping complete. CSV saved.')
