import yaml
import requests

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

query_fields = config['query_fields']

params = {
    'access_token': config['access_token'],
    'ad_type': 'POLITICAL_AND_ISSUE_ADS',
    'ad_reached_countries': "['US']",
    'search_terms': config['search_terms'],
    'fields': ",".join(query_fields),
    'limit': config['page_total']
}

r = requests.get('https://graph.facebook.com/v5.0/ads_archive', params=params)
data = r.json()

print(data)