"""Main memorize server entry point."""
import datamuse
from fastapi import FastAPI
from matcher import AssociationsMatcher

app = FastAPI()


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
    if not word.isalpha() or word == "" or limit == 0:
        return {}

    if split:
        match = AssociationsMatcher(word, limit)
        await match.generate_possible_splits()
        return match.most_associative

    return await AssociationsMatcher.get_associations(word, limit)

@app.get("/definitions/{word}")
async def get_definition(word: str = ""):
    """Get definition of specific word.
        
        Using datamuse api.
        
        Notes:
            If the word is not exists, the definition
            will be the definition of the most closest word.
            It fixes spelling problems. 
            For example: Paralize -> Paralyze.
    """
    if word == "":
        return {"definitions": []}
    
    closest_word = await datamuse.get_closest_word(word)
   
    return {
        "word": closest_word.word,
        "definitions":
            closest_word.defs if "defs" in closest_word else []
    }
    

@app.get("/closest/{word}")
async def get_closest_word(word: str = ""):
    """Get closest word.
        
        Using datamuse api.
    """
    if word == "":
        return {"definitions": []}
    
    closest_word = await datamuse.get_closest_word(word)
   
    return {
        "word": closest_word.word,
    }