import yaml
import requests
import csv
import re

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

f1 = open('fb_ads.csv', 'w')

w1 = csv.DictWriter(f1, fieldnames=config['output_fields'],
                    extrasaction='ignore')
w1.writeheader()

r = requests.get('https://graph.facebook.com/v5.0/ads_archive',
                 params=params)
data = r.json()
for ad in data['data']:
    # The ad_id is encoded in the ad snapshot URL
    # and cannot be accessed as a normal field. (?!?!)

    ad_id = re.search(r'\d+', ad['ad_snapshot_url']).group(0)
    ad_url = 'https://www.facebook.com/ads/library/?id=' + ad_id
    ad.update({'ad_id': ad_id,
               'ad_url': ad_url})
    w1.writerow(ad)

f1.close()
