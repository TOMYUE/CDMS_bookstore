from fastapi import FastAPI
from fastapi.requests import *
from fastapi.responses import JSONResponse
from be.model import user
from pydantic import BaseModel
import sqlalchemy

app = FastAPI()

class LoginForm(BaseModel):
    user_id: int
    password: str
    terminal: str

@app.post("/login")
def login(form: LoginForm):
    u = user.User()
    code, message, token = u.login(
        user_id=form.user_id, 
        password=form.password, 
        terminal=form.terminal
    )
    return JSONResponse({"message": message, "token": token}, status_code=code)


class LogoutForm(BaseModel):
    user_id: int
    token: str

@app.post("/logout")
def logout(form: LogoutForm):
    u = user.User()
    code, message = u.logout(
        user_id=user_id,
        token=token
    )
    return JSONResponse({"message":message},status_code=code)


class RegisterForm(BaseModel):
    user_id: int
    uname: str
    password: str

@app.post("/register")
def register(form:RegisterForm):
    u = user.User()
    code, message = u.register(
        user_id=form.user_id,
        uname=form.uname,
        password=form.password
    )
    return JSONResponse({"message":message}, status_code=code)


class UnregisterForm(BaseModel):
    user_id: int
    password: str

@app.post("/unregister")
def unregister(form:UnregisterForm):
    u = user.User()
    code, message = u.unregister(
        user_id=user_id,
        password=password
    )
    return JSONResponse({"message":message},status_code=code)

class ChangePwdForm(BaseModel):
    user_id: int
    old_password: str
    new_password: str

@app.post("/password")
def change_password(form: ChangePwdForm):
    u = user.User()
    code, message = u.change_password(
        user_id=user_id,
        old_password=old_password,
        new_password=new_password
    )
    return JSONResponse({"message":message},status_code=code)
