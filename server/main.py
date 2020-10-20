"""Main memorize server entry point."""
import datamuse
from fastapi import FastAPI
from matcher import AssociationsMatcher

app = FastAPI()


@app.get("/associations/{word}")
async def associate_word(word: str = ""):
    # TODO: Check empty word and other usecases.
    if word == "":
        return {}
    match = AssociationsMatcher(word)
    await match.generate_possible_splits()
    return match.most_associative

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
    # TODO: Check empty word and other usecases.
    if word == "":
        return {"definitions": []}
    
    closest_word = await datamuse.get_closest_word(word)
   
    return {
        "word": closest_word.word,
        "definitions":
            closest_word.defs if "defs" in closest_word else []
    }