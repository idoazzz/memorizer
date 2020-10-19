"""Datamuse api pythonic wrapper."""
from attrdict import AttrDict
import requests_async as requests

API_BASE_URL = "https://api.datamuse.com/words"

async def get_soundlike_words(word, metadata_flags="f"):
    """Request soundlike words.
    
    Notes:
        "f" flag stands for frequency of the words.
    """
    response = await requests.get(f"{API_BASE_URL}", params={
        "sl": word,
        "md": metadata_flags 
    })       
    return list(map(AttrDict, response.json()))

async def get_closest_word(word, definitions=True):
    """Request closest soundlike word definition."""
    if definitions:
        words = await get_soundlike_words(word, 
                                      metadata_flags="d")
    else:
        words = await get_soundlike_words(word)
    return words[0]

def extract_frequency(frequency):
    """Extract nemeric frequency from Datamuse metadata format."""
    return float(frequency[0][2:])