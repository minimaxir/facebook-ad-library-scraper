import yaml
import requests
import csv

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

params = {
    'access_token': config['access_token'],
    'ad_type': 'POLITICAL_AND_ISSUE_ADS',
    'ad_reached_countries': "['US']",
    'search_terms': config.get('search_terms'),
    'fields': ",".join(config['query_fields']),
    'limit': config['page_total']
}

with open('fb_ads.csv', 'w') as f1:
    w1 = csv.DictWriter(f1, fieldnames=config['output_fields'],
                        extrasaction='ignore')
    w1.writeheader()

    r = requests.get('https://graph.facebook.com/v5.0/ads_archive',
                     params=params)
    data = r.json()
    for ad in data['data']:
        w1.writerow(ad)
