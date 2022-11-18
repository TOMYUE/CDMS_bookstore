from fastapi import FastAPI
from be.model import seller
import json

app = FastAPI()

@app.post("/create_store")
def seller_create_store():
    raise "Not implemented yet"

@app.post("/add_book")
def seller_add_book():
    raise "Not implemented yet"

@app.post("/add_stock_level")
def add_stock_level():
    raise "Not implemented yet"

