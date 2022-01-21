from requests import Session, Request
import os, json

session = Session()

BASE_URL: str = 'www.target.com'

API_URL: str = 'redsky.target.com'

VERIFY: bool = False

HEADERS = {
    'Accept': 'application/json, text/plain',
    'Origin': f'https://{BASE_URL}',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': f'https://{BASE_URL}',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'sec-ch-ua-platform': 'Windows',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
}

# GET API KEY
url = f'https://{BASE_URL}/'
request = Request('GET', url=url, headers=HEADERS)
req = session.prepare_request(request)
response = session.send(req, verify=VERIFY)
api_key = response.text.split('"apiKey":"')[1].split('"')[0]
location = response.cookies.get('GuestLocation').split('|')[0]

# GET LOCATION
url = f'https://{API_URL}/v3/stores/nearby/{location}?key={api_key}&limit=1&within=100&unit=mile'
request = Request('GET', url=url, headers=HEADERS)
req = session.prepare_request(request)
response = session.send(req, verify=VERIFY).json()
if len(response) == 0:
    raise ValueError('Invalid location')
location = response[0].get('locations')[0].get('location_id')

# SET DEFAULT
"""IN THE URL OF THE DEMO, YOU CAN SEE THESE VALUES"""
item = 84616123
product = 84240109

# GET ITEM
url = f'https://{API_URL}/redsky_aggregations/v1/web/pdp_client_v1?key={api_key}&tcin={item}&pricing_store_id={location}&has_financing_options=true&has_size_context=true'
request = Request('GET', url=url, headers=HEADERS)
req = session.prepare_request(request)
response = session.send(req, verify=VERIFY).json()
products = {int(a.get('tcin')): a for a in response.get('data', {}).get('product', {}).get('children', [])}

# GET VALUES
item = products[product]
with open('response.json', 'w', encoding='utf-8') as f:
    json.dump(item, f, ensure_ascii=False, indent=4)