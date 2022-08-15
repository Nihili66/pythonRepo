from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from peewee import Model
from peewee import SqliteDatabase
from peewee import CharField
from jose import jwt


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


app = FastAPI()

templates = Jinja2Templates(directory='./templates')
users_db = SqliteDatabase('users_db.db')
users_db.connect()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Token(Model):
    access_token = CharField()
    token_type = CharField()
    username = CharField()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class Users(Model):
    username = CharField()
    password = CharField()

    class Meta:
        database = users_db


@app.get("/")
def home_page(request: Request,):
    return templates.TemplateResponse('back.html', context={'request': request})


@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse('register.html', context={'request': request})

@app.post("/register")
def register_page(request: Request, username: str = Form(), password: str = Form()):
    new_user = Users(username=username, password=password)
    new_user.save()
    return templates.TemplateResponse('reg_success.html', context={'request': request, 'username': username, 'password': password})


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})


@app.post("/login")
def login(request: Request, username: str = Form(), password: str = Form()):
    login_user = Users.select().where(Users.username == username and Users.password == password)
    if not login_user.exists():
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token({"sub": username})
    templates.TemplateResponse('home.html', context={'request': request, 'username': username, 'password': password})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/location")
def location_page():
    return "Here you will be able to check your location"


@app.get("/weather")
def weather_page():
    return "Here you will be able to check weather"
