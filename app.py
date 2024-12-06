from sqlalchemy.orm import Session

from config import app, templates
from db import get_db, User

from fastapi.responses import HTMLResponse
from fastapi import Request, Depends

@app.get('/', response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
