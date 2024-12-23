from sqlalchemy.orm import Session

from config import app, templates
from db import get_db, User
from sqlalchemy.exc import IntegrityError
from functools import wraps

from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import Request, Depends, Form


def login_required(view):
    @wraps(view)
    async def wrapped(request: Request, *args, db: Session, **kwargs):
        if not request.session.get('is_authenticated', False):
            return RedirectResponse('/login')
        return await view(request, *args, db=db, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    async def wrapped(request: Request, *args, db: Session, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return RedirectResponse('/login')

        user = db.query(User).filter_by(id=user_id).first()
        if not user or not user.is_admin:
            return JSONResponse(content={"error": "Don't have permission"}, status_code=403)

        return await view(request, *args, db=db, **kwargs)
    return wrapped


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    user = db.query(User).filter(User.id == user_id).first() if user_id else None
    if user and user.is_admin:
        return templates.TemplateResponse("index-admin.html", {"request": request})
    elif user:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return templates.TemplateResponse("index.html", {"request": request})


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


@app.post('/login')
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username, password=password).first()
    if user is None:
        return RedirectResponse('/login', status_code=303)
    request.session['is_authenticated'] = True
    request.session['user_id'] = user.id
    return RedirectResponse('/', status_code=303)


@app.get('/is-admin', response_class=HTMLResponse)
@login_required
@admin_required
async def get_is_admin_page(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse('is-admin.html', {'request': request, 'users': users})


@app.post('/is-admin')
@login_required
@admin_required
async def update_admins(is_admin: list[int] = Form([]), db: Session = Depends(get_db)):
    users = db.query(User).all()
    for user in users:
        user.is_admin = user.id in is_admin
    db.commit()
    return RedirectResponse('/is-admin', status_code=303)