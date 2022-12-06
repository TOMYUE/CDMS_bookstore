from fastapi import FastAPI
from fastapi.requests import *
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlalchemy
from typing import *
from relations import user

app = FastAPI()

class LoginForm(BaseModel):
    uname: str
    password: str
    terminal: str

@app.post("/seller/login")
async def seller_login(form: LoginForm):
    code, message, token = user.seller_login(
        form.uname,
        form.password,
        form.terminal
    )
    return JSONResponse({"message": message, "token": token}, status_code=code)

@app.post("/buyer/login")
async def buyer_login(form: LoginForm):
    code, message, token = user.buyer_login(
        form.uname,
        form.password,
        form.terminal
    )
    return JSONResponse({"message": message, "token": token}, status_code=code)


class LogoutForm(BaseModel):
    uname: str
    token: str

@app.post("/seller/logout")
async def seller_logout(form: LogoutForm):
    code, message = user.seller_logout(
        form.uname,
        form.token
    )
    return JSONResponse({"message":message},status_code=code)

@app.post("/buyer/logout")
async def buyer_logout(form: LogoutForm):
    code, message = user.buyer_logout(
        form.uname,
        form.token
    )
    return JSONResponse({"message":message},status_code=code)


class RegisterForm(BaseModel):
    uname: str
    password: str
    account: str
    balance: float
    token: str
    terminal: str

@app.post("/seller/register")
async def seller_register(form:RegisterForm):
    code, message, uid = user.seller_register(
        form.uname,
        form.password,
        form.account,
        form.balance,
        form.token,
        form.terminal
    )
    return JSONResponse({"message":message,"uid":uid}, status_code=code)

@app.post("/buyer/register")
async def buyer_register(form:RegisterForm):
    code, message, uid = user.buyer_register(
        form.uname,
        form.password,
        form.account,
        form.balance,
        form.token,
        form.terminal
    )
    return JSONResponse({"message":message, "uid":uid}, status_code=code)


class UnregisterForm(BaseModel):
    uname: str
    password: str

@app.post("/seller/unregister")
async def seller_unregister(form:UnregisterForm):
    code, message = user.seller_unregister(
        form.uname,
        form.password
    )
    return JSONResponse({"message":message},status_code=code)

@app.post("/buyer/unregister")
async def seller_unregister(form:UnregisterForm):
    code, message = user.buyer_unregister(
        form.uname,
        form.password
    )
    return JSONResponse({"message":message},status_code=code)

class ChangePwdForm(BaseModel):
    uname: str
    old_password: str
    new_password: str

@app.post("/seller/password")
async def sellse_change_password(form: ChangePwdForm):
    code, message = user.seller_change_password(
        form.uname,
        form.old_password,
        form.new_password
    )
    return JSONResponse({"message":message},status_code=code)

@app.post("/buyer/password")
async def buyer_change_password(form: ChangePwdForm):
    code, message = user.buyer_change_password(
        form.uname,
        form.old_password,
        form.new_password
    )
    return JSONResponse({"message":message},status_code=code)


class searchtitleGlobForm(BaseModel):
    title: str
    page: int

@app.post("/search_title")
async def search_title(form:searchtitleGlobForm):
    code, msg = user.search_title(form.title, form.page)
    return JSONResponse({"message": msg}, status_code=code)

class searchtitleLocalForm(BaseModel):
    title:str
    page:int
    sid:int

@app.post("/search_title_in_store")
async def search_title_in_store(form:searchtitleLocalForm):
    code, msg = user.search_title_in_store(form.title, form.page, form.sid)
    return JSONResponse({"message": msg}, status_code=code)

class searchtagGlobForm(BaseModel):
    tag: str
    page: int

@app.post("/search_tag")
async def search_tag(form:searchtagGlobForm):
    code, msg = user.search_tag(form.tag, form.page)
    return JSONResponse({"message":msg},status_code=code)


class searchtagLocalForm(BaseModel):
    tag: str
    page: int


@app.post("/search_tag_in_store")
async def search_tag_in_store(form: searchtagLocalForm):
    code, msg = user.search_tag_in_store(form.tag, form.page, form.sid)
    return JSONResponse({"message": msg}, status_code=code)


class searchcontentGlobForm(BaseModel):
    book_intro: str
    page: int

@app.post("/search_content")
async def search_content(form:searchcontentGlobForm):
    code, msg = user.search_content(form.book_intro, form.page)
    return JSONResponse({"message":msg},status_code=code)

class searchcontentLocalForm(BaseModel):
    book_intro: str
    page: int
    sid: int

@app.post("/search_content_in_store")
async def search_content_in_store(form:searchcontentLocalForm):
    code, msg = user.search_content_in_store(form.book_intro, form.page, form.sid)
    return JSONResponse({"message":msg},status_code=code)

class searchauthorGlobForm(BaseModel):
    author: str
    page: int

@app.post("/search_author")
async def search_author(form: searchauthorGlobForm):
    code, msg = user.search_author(form.author, form.page)
    return JSONResponse({"message":msg},status_code=code)


class searchauthorLocalForm(BaseModel):
    author: str
    page: int
    sid: int

@app.post("/search_author_in_store")
async def search_author(form: searchauthorLocalForm):
    code, msg = user.search_author_in_store(form.author, form.page, form.sid)
    return JSONResponse({"message":msg},status_code=code)
