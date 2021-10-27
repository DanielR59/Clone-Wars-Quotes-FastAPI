from fastapi import FastAPI, HTTPException
import json
from random import randint
with open('conewarsquotes.json','r') as f:
    data = json.load(f)

app = FastAPI()

@app.get('/all_quotes/')
def get_all():
    return data


@app.get('/random_quote/')
def get_random_quote(language : str = "eng", just_quote : bool = True):
    quote_id = randint(1,132)
    for element in data:
        # print(element)
        if element["id"] == quote_id:
            if just_quote:
                return element["quote"]
            else:
                return element
    raise HTTPException(status_code=404,detail="Quote not found")

@app.get('/quotes/')
def get_quote_by_chapter_season(season : int, chapter:int, language :str = "eng"):
    for element in data:
        print(element)
        if element["season"] == season and element["chapter"] == chapter:
            return element
    raise HTTPException(status_code=404, detail="Chapter not found") 

 