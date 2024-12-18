from sqlalchemy.orm import Session

from config import app, templates
from db import get_db, User
from sqlalchemy.exc import IntegrityError

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Depends, Form


@app.get('/', response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post('/register')
async def register(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
        db: Session = Depends(get_db)
):
    user = User(username=username, password=password, email=email)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        return RedirectResponse('/register?is_invalid_data=True', status_code=303)

    return RedirectResponse('/', status_code=303)


@app.get('/login', response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})
