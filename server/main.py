"""Main memorize server entry point."""
import datamuse
from fastapi import FastAPI
from associations import get_associations
from auto_splitter import get_auto_splits_associations

app = FastAPI()

def valid_word(word):
    """Check if the word is valid."""
    return word.isalpha() and word != ""

@app.get("/associations/{word}")
async def associate_word(word: str = "", limit: int = 10, 
                         split: bool = True):
    """Get specific word associations.

    Args:
        word (str, optional): Target word. Defaults to "".
        limit (int, optional): Associations limit. Defaults to 10.
        split (bool, optional): Should the word be splitted. Defaults to True.

    Notes:
        If the split flag is on the word will be splitted by the backend.
        The split will be the most associative by grades.
    
    Returns:
        json. Associations with extra metadata.
    """
    if not valid_word(word) or limit == 0:
        return {}
    
    if split:
        pair = await get_auto_splits_associations(word, limit)
        return { 
            "splits": [word_associations.to_dictionary() for 
                       word_associations in pair] 
        }
        
    # Get the first and only association.
    result = await get_associations([word], limit)
    word_associations = result.pop()
    return { "splits": [word_associations.to_dictionary()] }

@app.get("/definitions/{word}")
async def get_definition(word: str = ""):
    """Get definition of specific word.
        
    Notes:
        If the word is not exists, the definition
        will be the definition of the most closest word.
        It fixes spelling problems. 
        For example: Paralize -> Paralyze.
    """
    if not valid_word(word):
        return {"definitions": []}
    
    result = await datamuse.get_closest_word(word)
    return {
        "word": result.word,
        "definitions":
            result.defs if "defs" in result else []
    }
    

@app.get("/closest/{word}")
async def get_closest_word(word: str = ""):
    """Get closest word.
        
        Using datamuse api.
    """
    if not valid_word(word):
        return {"definitions": []}
    
    closest_word = await datamuse.get_closest_word(word)
    return {
        "word": closest_word.word,
    }