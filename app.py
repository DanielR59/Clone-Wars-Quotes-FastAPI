from fastapi import FastAPI, HTTPException, Request, Query
import json
# from typing import Optional
from random import randint
from starlette.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

with open('clonewarsquotes_eng.json','r') as f:
    data = json.load(f)
with open('clonewarsquotes_esp.json','r') as f:
    data_esp = json.load(f)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get('/')
def root():
        return RedirectResponse(url='/en')

@app.get('/{lang}')
def root(request : Request, lang : str = Query("en",enumerate=["en","es"])):
    if lang:
        return templates.TemplateResponse("index.html",{"request" : request,"quote": get_random_quote(lang=lang)})
    else:
        return templates.TemplateResponse("index.html",{"request" : request,"quote": get_random_quote(lang="en")})

@app.get('/all_quotes/')
def get_all(lang : str = Query("en",enum=["en","es"])):
    if lang == "en": 
        return data
    if lang == "es": 
        return data_esp

@app.get('/random_quote/')
def get_random_quote(lang : str = Query("en",enum=["en","es"]), just_quote : bool = True):
    if lang == "en":            
        quote_id = randint(1,128) #Son 132, pero los ultimos capitulos no tienen
        for element in data:
            # print(element)
            if element["id"] == quote_id:
                if just_quote:
                    return element["quote"]
                else:
                    return element
    if lang == "es":            
        quote_id = randint(1,120) #Son 120 falta hacer mejor scrapping
        for element in data_esp:
            # print(element)
            if element["id"] == quote_id:
                if just_quote:
                    return element["quote"]
                else:
                    return element
    raise HTTPException(status_code=404,detail="Quote not found")
@app.get('/quotes/')
def get_quote_by_chapter_season(season : int = Query(...,gt=0,le=7), chapter:int = Query(...,gt=0,le=22), lang :str = Query("en",enum=["en","es"]), just_quote : bool = True):
    if lang == "en":

        for element in data:
            if element["season"] == season and element["chapter"] == chapter:
                if just_quote:
                    return element["quote"]
                else:
                    return element
    if lang == "es":

        for element in data_esp:
            if element["season"] == season and element["chapter"] == chapter:
                if just_quote:
                    return element["quote"]
                else:
                    return element
    raise HTTPException(status_code=404, detail="Chapter not found") 

 