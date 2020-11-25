"""Datamuse api pythonic wrapper."""
from attrdict import AttrDict
import requests_async as requests

API_BASE_URL = "https://api.datamuse.com/words"

async def get_soundlike_words(word, metadata_flags="fd"):
    """Request soundlike words.
    
    Notes:
        "f" flag stands for frequency of the words.
        "d" flag stands for definition of the words.
        The results returned sorted by score.
    """
    response = await requests.get(f"{API_BASE_URL}", params={
        "sl": word,
        "md": metadata_flags 
    })     
    return [fetched_word for fetched_word in 
            list(map(AttrDict, response.json()))
            if fetched_word.word.isalpha() and len(fetched_word.word) > 1]

async def get_closest_word(word, definitions=True):
    """Request closest soundlike word definition."""
    words = await get_soundlike_words(word)
    return words[0]

def extract_frequency(frequency):
    """Extract nemeric frequency from Datamuse metadata format."""
    return float(frequency[0][2:])