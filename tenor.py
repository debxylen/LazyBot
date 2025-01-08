import requests
import random
import os
from dotenv import load_dotenv
from predefined_gifs import gifs as predefined_gifs

load_dotenv()

def get_gif(tags, limit=100, currentGif=None):
    """
    Fetches a GIF URL based on the provided tags and pagination state.

    @param tags: str
        A string containing the search tags (e.g., "hug", "wave").
        Tags are concatenated to the base query for more specific results.
    @param limit: int, default=100
        The maximum number of GIFs to fetch in the response.
    @param currentGif: dict
        A dictionary containing the current pagination state:
        {
            "startingPoint": int,  # Index of the GIF to fetch within the result set
            "currentPage": str     # Pagination token for the API
        }

    @return: tuple
        Returns a tuple containing:
        - The URL of the selected GIF (str)
        - The next pagination token (str) for fetching subsequent results
    """

    # Extract pagination data from currentGif
    starting = int(currentGif["startingPoint"])
    currentPage = currentGif["currentPage"]

    # API Configuration
    api_key = os.getenv('TENOR_KEY')
    client_key = os.getenv('TENOR_CLIENT')
    base_url = 'https://tenor.googleapis.com/v2/search'


    # API Parameters
    params = {
        'q': f'anime+{tags}',
        'key': api_key,
        'client_key': client_key,
        'limit': limit,
        'pos': currentPage
    }
    
    # Perform the API call
    response = requests.get(base_url, params=params)

    # filtered_gifs = []
    if response.status_code==200:
        # Parse the response JSON
        data= response.json()
        results = data.get("results", [])
        next = data.get("next", "")
        currentGif = results[starting]['media_formats']['gif']['url']
     
        return currentGif, next
