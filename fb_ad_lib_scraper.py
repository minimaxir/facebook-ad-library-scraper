import yaml
import requests
import csv
import re
from tqdm import tqdm

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

assert config['search_total'] % config['page_total'] == 0, \
    "search_total should be a multiple of page_total."

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

pbar = tqdm(total=config['search_total'], smoothing=0)

for _ in range(int(config['search_total'] / config['page_total'])):
    r = requests.get('https://graph.facebook.com/v5.0/ads_archive',
                     params=params)
    data = r.json()
    for ad in data['data']:
        # The ad_id is encoded in the ad snapshot URL
        # and cannot be accessed as a normal field. (?!?!)

        ad_id = re.search(r'\d+', ad['ad_snapshot_url']).group(0)
        ad_url = 'https://www.facebook.com/ads/library/?id=' + ad_id
        ad.update({'ad_id': ad_id,
                   'ad_url': ad_url,
                   'impressions_min': ad['impressions']['lower_bound'],
                   'impressions_max': ad['impressions']['upper_bound'],
                   'spend_min': ad['spend']['lower_bound'],
                   'spend_max': ad['spend']['upper_bound'],
                   })
        w1.writerow(ad)
        pbar.update()
    params.update({'after': data['paging']['cursors']['after']})

f1.close()
pbar.close()
