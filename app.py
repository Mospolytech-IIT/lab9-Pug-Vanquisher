from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from models import session, User, Post, engine
import traceback
from sqlalchemy.exc import IntegrityError

# Инициализация FastAPI
app = FastAPI()

# Подключение шаблонов
templates = Jinja2Templates(directory="templates")

# Подключение статики
app.mount("/static", StaticFiles(directory="static"), name="static")


# Главная страница
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# === CRUD для Users ===

@app.get("/users")
async def list_users(request: Request):
    users = session.query(User).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/users/new")
async def new_user_form(request: Request):
    return templates.TemplateResponse("user_form.html", {"request": request})


@app.post("/users/new")
async def create_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    new_user = User(username=username, email=email, password=password)
    try:
        session.add(new_user)
        session.commit()
        return RedirectResponse("/users", status_code=303)
    except IntegrityError as e:
        session.rollback()  # Откат при ошибке
        error_message = "Дурак, пиши уникальные значения!"
        return templates.TemplateResponse("user_form.html", {"request": request, "error_message": error_message})


@app.get("/users/edit/{user_id}")
async def edit_user_form(request: Request, user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user_form.html", {"request": request, "user": user})


@app.post("/users/edit/{user_id}")
async def update_user(request: Request, user_id: int, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    user.email = email
    user.password = password
    try:
        session.commit()
        return RedirectResponse("/users", status_code=303)
    except IntegrityError as e:
        session.rollback()  # Откат при ошибке
        error_message = "Дурак, пиши уникальные значения"
        return templates.TemplateResponse("user_form.html", {"request": request, "user": user, "error_message": error_message})


@app.get("/users/delete/{user_id}")
async def delete_user(user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.query(Post).filter(Post.user_id == user_id).delete()
    session.delete(user)
    session.commit()
    return RedirectResponse("/users", status_code=303)


# === CRUD для Posts ===

@app.get("/posts")
async def list_posts(request: Request):
    posts = session.query(Post).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})


@app.get("/posts/new")
async def new_post_form(request: Request):
    users = session.query(User).all()
    return templates.TemplateResponse("post_form.html", {"request": request, "users": users})


@app.post("/posts/new")
async def create_post(title: str = Form(...), content: str = Form(...), user_id: int = Form(...)):
    new_post = Post(title=title, content=content, user_id=user_id)
    session.add(new_post)
    session.commit()
    return RedirectResponse("/posts", status_code=303)


@app.get("/posts/edit/{post_id}")
async def edit_post_form(request: Request, post_id: int):
    post = session.query(Post).filter(Post.id == post_id).first()
    users = session.query(User).all()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("post_form.html", {"request": request, "post": post, "users": users})


@app.post("/posts/edit/{post_id}")
async def update_post(post_id: int, title: str = Form(...), content: str = Form(...), user_id: int = Form(...)):
    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = title
    post.content = content
    post.user_id = user_id
    session.commit()
    return RedirectResponse("/posts", status_code=303)


@app.get("/posts/delete/{post_id}")
async def delete_post(post_id: int):
    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return RedirectResponse("/posts", status_code=303)
