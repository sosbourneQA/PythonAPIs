import requests
import json
import requests_cache
import time
from IPython.core.display import clear_output

requests_cache.install_cache()

# headers = {
#     'user-agent': 'Dataquest'
# }

# r = requests.get('http://my-api-url', headers=headers)

API_KEY = "11a517fe80f993232844d09c492563d1";
USER_AGENT = "Dataquest";

# headers = {
#     'user-agent': USER_AGENT
# }
#
# payload = {
#     'api_key': API_KEY,
#     'method': 'chart.gettopartists',
#     'format': 'json'
# }

# r = requests.get('http://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
# print(r.status_code)

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


r = lastfm_get({
    'method': 'chart.gettopartists'
})

print(r.status_code)

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# jprint(r.json())
# jprint(r.json()['artists']['@attr'])






responses = []

page = 1
total_pages = 99999 # this is just a dummy number so the loop starts

while page <= total_pages:
    payload = {
        'method': 'chart.gettopartists',
        'limit': 500,
        'page': page
    }

    # print some output so we can see the status
    print("Requesting page {}/{}".format(page, total_pages))
    # clear the output to make things neater
    clear_output(wait = True)

    # make the API call
    response = lastfm_get(payload)

    # if we get an error, print the response and halt the loop
    if response.status_code != 200:
        print(response.text)
        break

    # extract pagination info
    page = int(response.json()['artists']['@attr']['page'])
    total_pages = int(response.json()['artists']['@attr']['totalPages'])

    # append response
    responses.append(response)

    # if it's not a cached result, sleep
    if not getattr(response, 'from_cache', False):
        time.sleep(0.25)

    # increment the page number
    page += 1