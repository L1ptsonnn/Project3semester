from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import Request, Depends, Form, File, UploadFile, HTTPException
from config import app, templates
from db import get_db, User, Tours
from sqlalchemy.exc import IntegrityError
import os
import shutil
from functools import wraps

UPLOAD_FOLDER = "static/pictures"

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

    tours = db.query(Tours).all()

    if user and user.is_admin:
        return templates.TemplateResponse("index-admin.html", {"request": request, "tours": tours})
    elif user:
        return templates.TemplateResponse("index.html", {"request": request, "tours": tours})
    else:
        return templates.TemplateResponse("index.html", {"request": request, "tours": tours})


@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post('/register')
async def register_post(
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
async def login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@app.post('/login')
async def login_post(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username, password=password).first()
    if user is None:
        return RedirectResponse('/login', status_code=303)
    request.session['is_authenticated'] = True
    request.session['user_id'] = user.id
    return RedirectResponse('/', status_code=303)


@app.get('/is-admin', response_class=HTMLResponse)
async def get_is_admin_page(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse('is-admin.html', {'request': request, 'users': users})


@app.post('/is-admin')
async def update_admins(is_admin: list[int] = Form([]), db: Session = Depends(get_db)):
    users = db.query(User).all()
    for user in users:
        user.is_admin = user.id in is_admin
    db.commit()
    return RedirectResponse('/', status_code=303)


@app.get("/tour-create", response_class=HTMLResponse)
async def tour_create(request: Request):
    return templates.TemplateResponse("tour-create.html", {"request": request})


@app.post("/tour-create")
async def create_tour(
        country: str = Form(...),
        content: str = Form(...),
        group_size: int = Form(...),
        price: int = Form(...),
        image: UploadFile = File(None),
        db: Session = Depends(get_db)
):
    image_path = "static/pictures/default_tour.png"

    if image:
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    new_tour = Tours(
        country=country,
        content=content,
        group_size=group_size,
        price=price,
        image=image_path
    )

    db.add(new_tour)
    db.commit()

    return RedirectResponse(url='/', status_code=302)


@app.post("/edit-tour/{tour_id}")
async def edit_tour(tour_id: int, country: str = Form(...), content: str = Form(...), group_size: int = Form(...),
                    price: int = Form(...), image: UploadFile = File(None), db: Session = Depends(get_db)):

    tour = db.query(Tours).filter(Tours.id == tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")

    if image:
        image_path = f"static/pictures/{image.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        tour.image = image_path

    tour.country = country
    tour.content = content
    tour.group_size = group_size
    tour.price = price

    db.commit()
    db.refresh(tour)

    return RedirectResponse(url="/", status_code=303)



@app.post('/delete-tour/{tour_id}')
async def delete_tour(tour_id: int, db: Session = Depends(get_db)):
    tour_to_delete = db.query(Tours).filter(Tours.id == tour_id).first()
    if not tour_to_delete:
        raise HTTPException(status_code=404, detail="Tour not found")
    db.delete(tour_to_delete)
    db.commit()
    return RedirectResponse(url="/", status_code=303)