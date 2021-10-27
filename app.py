from fastapi import FastAPI, HTTPException, Request, Query
import json
from random import randint
from starlette.responses import FileResponse 
from fastapi.templating import Jinja2Templates

with open('clonewarsquotes_eng.json','r') as f:
    data = json.load(f)
templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get('/')
def root(request : Request):
    return templates.TemplateResponse("index.html",{"request" : request,"quote": get_random_quote()})


@app.get('/all_quotes/')
def get_all():
    return data


@app.get('/random_quote/')
def get_random_quote(language : str = "eng", just_quote : bool = True):
    quote_id = randint(1,128) #Son 132, pero los ultimos capitulos no tienen
    for element in data:
        # print(element)
        if element["id"] == quote_id:
            if just_quote:
                return element["quote"]
            else:
                return element
    raise HTTPException(status_code=404,detail="Quote not found")

@app.get('/quotes/')
def get_quote_by_chapter_season(season : int = Query(...,gt=0,le=7), chapter:int = Query(...,gt=0,le=22), language :str = "eng", just_quote : bool = True):
    for element in data:
        print(element)
        if element["season"] == season and element["chapter"] == chapter:
            if just_quote:
                return element["quote"]
            else:
                return element
    raise HTTPException(status_code=404, detail="Chapter not found") 

 