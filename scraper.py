import requests, json
import pandas as pd
import os
import time

API = "https://fdx-api.sportsbook.fanduel.com/api/v1/pulse/cards/MD/location/live"

def get_fd_mlb():
    resp = requests.get(API, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    rows = []

    # find the baseball cards
    for card in data['cards']:
        if card.get('sport') != 'Baseball':
            continue
        for ev in card['events']:
            away, home = (c['name'] for c in ev['competitors'])
            ml_legs = [l for l in ev['legs'] if l['marketType'] == 'MONEY_LINE']
            
            if len(ml_legs) != 2:
                continue

            away_leg, home_leg = ml_legs

            rows.append({
                'platform':'fd',
                'away': away_leg['description'].replace(' to win', ''),
                'home': home_leg['description'].replace(' to win', ''),
                'away_ml': away_leg['americanOdds'],
                'home_ml': home_leg['americanOdds'],
                'collected_at': datetime.utcnow().isoformat()
            })
        break

    return rows

def write_fd_csv(rows):
    fn = "data/csv/fd.csv"
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(
        fn,
        mode= 'a',
        header= not os.path.exists(fn),
        index= False
    )
    
if __name__ == '__main__':
    INTERVAL = 60
    while True:
        try:
            rows = get_fd_mlb()
            write_fd_csv(rows)
            print(f" scraped @ {time.strftime('%X')}")
        except Exception as e:
            print('ERROR', e)
        time.sleep(INTERVAL)