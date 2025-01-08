import requests
from dotenv import load_dotenv
load_dotenv()

def get_gif(tags: list):
    api_key = os.getenv('TENOR_API_KEY')
    base_url = 'https://api.tenor.com/v1/search'

    params = {
        'q': ', '.join(tags),
        'key': api_key,
        'limit': 1
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        gif_url = data['results'][0]['media'][0]['gif']['url']
        return gif_url
    else:
        raise Exception("Error fetching GIFs: " + response.status_code + response.text)
