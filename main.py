from typing import Optional

import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Form
from gen_xpath import Test
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from loguru import logger
import os



tmp = Jinja2Templates(directory='templates')


class Item(BaseModel):
    html: str
    strings: str


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/xpath', response_class=HTMLResponse)
def read_root(request: Request):
    return tmp.TemplateResponse('index.html', {'request': request})


@app.post('/xpath')
async def xpath(request: Request, item: Item):
    html = item.html
    strings = item.strings
    try:
        t = Test(strings, html)
        result = t.start()
        logger.info(result)
        if result:
            return {'code': 2, 'data': result}
        else:
            return {'code': 1}
    except Exception as e:
        logger.error(e)
        return {'code': 0}


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, debug=True)
