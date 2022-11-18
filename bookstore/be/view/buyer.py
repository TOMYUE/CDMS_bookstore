from fastapi import FastAPI
from be.model.buyer import Buyer
from typing import *
from typing_extensions import *

app = FastAPI()

@app.post("/new_order")
def new_order():
    return "No yet implemented"


@app.post("/payment")
def payment():
    return "No yet implemented"


@app.post("/add_funds")
def add_funds():
    return "No yet implemented"
