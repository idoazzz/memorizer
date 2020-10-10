from fastapi import FastAPI
from matcher import AssociationsMatcher

app = FastAPI()

@app.get("/{word}")
def associate_word(word: str):
    if word == "":
        return {}
    match = AssociationsMatcher(word).most_associative
    return match