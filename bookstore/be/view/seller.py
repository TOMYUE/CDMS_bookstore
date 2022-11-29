from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from be.relations import seller
from typing import *

app = FastAPI()

class CreateStoreForm(BaseModel):
    user_id: int
    store_id: int

@app.post("/create_store")
async def seller_create_store(form: CreateStoreForm):
    code, msg = seller.create_store(form.user_id, form.store_id)
    return JSONResponse({"message": msg}, code)

class BookInfo(BaseModel):
    tags: List[str] = list()
    pictures: List[bytes] = list()
    id: int
    title: str
    author: str
    publisher: str
    original_title: str
    translator: str
    pub_year: str
    pages: int
    price: int
    binding: str
    isbn: str
    author_intro: str
    book_intro: str
    content: str

class AddBookForm(BaseModel):
    book_info: BookInfo
    stock_level: int = 0
    user_id: int
    store_id: int

@app.post("/add_book")
async def seller_add_book(form: AddBookForm):
    code, msg = seller.add_book(form.user_id, form.store_id, form.stock_level, **form.book_info.dict())
    return JSONResponse({"message": msg}, code)

class AddStockLevelForm(BaseModel):
    user_id: int
    book_id: int
    store_id: int
    add_stock_level: int

@app.post("/add_stock_level")
async def add_stock_level(form: AddStockLevelForm):
    code, msg = seller.add_stock_level(form.user_id, form.store_id, form.book_id, form.add_stock_level)
    return JSONResponse({"message": msg}, code)
