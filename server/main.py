from fastapi import FastAPI
from matcher import AssociationsMatcher

app = FastAPI()

@app.get("/{word}")
async def associate_word(word: str):
    if word == "":
        return {}
    match = AssociationsMatcher(word)
    await match.generate_possible_splits()
    return match.most_associative