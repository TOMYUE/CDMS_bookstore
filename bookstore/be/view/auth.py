from fastapi import FastAPI
from fastapi.requests import *
from fastapi.responses import JSONResponse
from be.model import user
from pydantic import BaseModel

app = FastAPI()


class LoginForm(BaseModel):
    user_id: str
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


@app.post("/logout")
def logout():
    return "No yet implemented"


@app.post("/register")
def register():
    return "No yet implemented"

@app.post("/unregister")
def unregister():
    return "No yet implemented"

@app.post("/password")
def change_password():
    return "No yet implemented"
