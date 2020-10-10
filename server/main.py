from fastapi import FastAPI
from matcher import AssociationsMatcher

app = FastAPI()

@app.get("/{word}")
def associate_word(word: str):
    match = AssociationsMatcher(word).most_associative
    return match