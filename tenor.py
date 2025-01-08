import requests
import random
import os
from dotenv import load_dotenv
from predefined_gifs import gifs as predefined_gifs
load_dotenv()

def get_gif(tags, limit=100):
    api_key = os.getenv('TENOR_KEY')
    client_key = os.getenv('TENOR_CLIENT')
    base_url = 'https://tenor.googleapis.com/v2/search'

    params = {
        'q': tags,
        'key': api_key,
        'client_key': client_key,
        'limit': limit,
    }

    response = requests.get(base_url, params=params)

    filtered_gifs = []

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        for result in results:
            gif_tags = ''.join(result.get('tags', []))
            tag_matches = 0
            for tag in tags: tag_matches += 1 if tag in gif_tags else 0
            if tag_matches == len(tags): filtered_gifs.append(result['media_formats']['gif']['url'])

    # Add predefined GIFs as a fallback
    filtered_gifs.extend(predefined_gifs[tags[1]])
    # Convert to set and then to list to remove duplicates for absolutely no reason
    unique_gifs = list(set(filtered_gifs))
    # for i in unique_gifs: print(i)
    # Randomly choose one GIF
    return random.choice(unique_gifs)
