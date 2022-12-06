from fastapi import FastAPI
from fastapi.requests import *
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlalchemy
from typing import *
from relations import user

app = FastAPI()

class LoginForm(BaseModel):
    user_id: int
    password: str
    terminal: str

@app.post("/seller/login")
async def seller_login(form: LoginForm):
    code, message, token = user.seller_login(
        form.user_id,
        form.password,
        form.terminal
    )
    return JSONResponse({"message": message, "token": token}, status_code=code)

@app.post("/buyer/login")
async def buyer_login(form: LoginForm):
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
async def seller_logout(form: LogoutForm):
    code, message = user.seller_logout(
        form.user_id,
        form.token
    )
    return JSONResponse({"message":message},status_code=code)

@app.post("/buyer/logout")
async def buyer_logout(form: LogoutForm):
    code, message = user.buyer_logout(
        form.user_id,
        form.token
    )
    return JSONResponse({"message":message},status_code=code)


class RegisterForm(BaseModel):
    user_id: int
    uname: str
    password: str

@app.post("/seller/register")
async def seller_register(form:RegisterForm):
    code, message = user.seller_register(
        form.user_id,
        form.uname,
        form.password
    )
    return JSONResponse({"message":message}, status_code=code)

@app.post("/buyer/register")
async def buyer_register(form:RegisterForm):
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
async def seller_unregister(form:UnregisterForm):
    code, message = user.seller_unregister(
        form.user_id,
        form.password
    )
    return JSONResponse({"message":message},status_code=code)

@app.post("/buyer/unregister")
async def seller_unregister(form:UnregisterForm):
    code, message = user.buyer_unregister(
        form.user_id,
        form.password
    )
    return JSONResponse({"message":message},status_code=code)

class ChangePwdForm(BaseModel):
    user_id: int
    old_password: str
    new_password: str

@app.post("/seller/password")
async def sellse_change_password(form: ChangePwdForm):
    code, message = user.seller_change_password(
        form.user_id,
        form.old_password,
        form.new_password
    )
    return JSONResponse({"message":message},status_code=code)

@app.post("/buyer/password")
async def buyer_change_password(form: ChangePwdForm):
    code, message = user.buyer_change_password(
        form.user_id,
        form.old_password,
        form.new_password
    )
    return JSONResponse({"message":message},status_code=code)
