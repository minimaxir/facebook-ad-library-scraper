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
    'ad_active_status': config['ad_active_status'],
    'search_terms': config.get('search_terms'),
    'search_page_ids': ",".join(config.get('search_page_ids', [])),
    'fields': ",".join(config['query_fields']),
    'limit': config['page_total']
}

f1 = open('fb_ads.csv', 'w')
w1 = csv.DictWriter(f1, fieldnames=config['output_fields'],
                    extrasaction='ignore')
w1.writeheader()

f2 = open('fb_ads_demos.csv', 'w')
w2 = csv.DictWriter(f2, fieldnames=config['demo_fields'],
                    extrasaction='ignore')
w2.writeheader()

f3 = open('fb_ads_regions.csv', 'w')
w3 = csv.DictWriter(f3, fieldnames=config['region_fields'],
                    extrasaction='ignore')
w3.writeheader()

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

        # write to the unnested files
        for demo in ad['demographic_distribution']:
            demo.update({'ad_id': ad_id})
            w2.writerow(demo)

        for region in ad['region_distribution']:
            region.update({'ad_id': ad_id})
            w3.writerow(region)

        ad.update({'ad_id': ad_id,
                   'ad_url': ad_url,
                   'impressions_min': ad['impressions']['lower_bound'],
                   'impressions_max': ad['impressions']['upper_bound'],
                   'spend_min': ad['spend']['lower_bound'],
                   'spend_max': ad['spend']['upper_bound'],
                   })

        w1.writerow(ad)
        pbar.update()

    # if we have scraped all the ads, exit
    if 'paging' not in data:
        break

    params.update({'after': data['paging']['cursors']['after']})

f1.close()
f2.close()
f3.close()
pbar.close()
