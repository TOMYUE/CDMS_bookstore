from fastapi import FastAPI
from fastapi.requests import *
from fastapi.responses import JSONResponse
from be.model import user
from pydantic import BaseModel
import sqlalchemy
from typing import *
from be.relations import user

app = FastAPI()

class LoginForm(BaseModel):
    user_id: int
    password: str
    terminal: str

@app.post("/seller/login")
def seller_login(form: LoginForm):
    code, message, token = user.seller_login(
        form.user_id,
        form.password,
        form.terminal
    )
    return JSONResponse({"message": message, "token": token}, status_code=code)

@app.post("/buyer/login")
def buyer_login(form: LoginForm):
    code, message, token = user.buyer_login(
        form.user_id,
        form.password,
        form.terminal
    )
    return JSONResponse({"message": message, "token": token}, status_code=code)


class LogoutForm(BaseModel):
    user_id: int
    token: str

@app.post("/seller/logout")
def seller_logout(form: LogoutForm):
    code, message = user.seller_logout(
        user_id,
        token
    )
    return JSONResponse({"message":message},status_code=code)

@app.post("/buyer/logout")
def buyer_logout(form: LogoutForm):
    code, message = user.buyer_logout(
        user_id,
        token
    )
    return JSONResponse({"message":message},status_code=code)


class RegisterForm(BaseModel):
    user_id: int
    uname: str
    password: str

@app.post("/seller/register")
def seller_register(form:RegisterForm):
    code, message = user.seller_register(
        form.user_id,
        form.uname,
        form.password
    )
    return JSONResponse({"message":message}, status_code=code)

@app.post("/buyer/register")
def buyer_register(form:RegisterForm):
    code, message = user.buyer_register(
        form.user_id,
        form.uname,
        form.password
    )
    return JSONResponse({"message":message}, status_code=code)


class UnregisterForm(BaseModel):
    user_id: int
    password: str

@app.post("/seller/unregister")
def seller_unregister(form:UnregisterForm):
    code, message = user.seller_unregister(
        user_id,
        password
    )
    return JSONResponse({"message":message},status_code=code)

@app.post("/buyer/unregister")
def seller_unregister(form:UnregisterForm):
    code, message = user.buyer_unregister(
        user_id,
        password
    )
    return JSONResponse({"message":message},status_code=code)

class ChangePwdForm(BaseModel):
    user_id: int
    old_password: str
    new_password: str

@app.post("/seller/password")
def sellse_change_password(form: ChangePwdForm):
    code, message = user.seller_change_password(
        user_id,
        old_password,
        new_password
    )
    return JSONResponse({"message":message},status_code=code)

@app.post("/buyer/password")
def buyer_change_password(form: ChangePwdForm):
    code, message = user.buyer_change_password(
        user_id,
        old_password=old_password,
        new_password
    )
    return JSONResponse({"message":message},status_code=code)
