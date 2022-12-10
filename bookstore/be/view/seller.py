from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from relations import seller
from typing import *

app = FastAPI()

class CreateStoreForm(BaseModel):
    user_id: int
    store_id: int

@app.post("/create_store")
async def seller_create_store(form: CreateStoreForm):
    code, msg = seller.create_store(form.user_id, form.store_id)
    return JSONResponse({"message": msg}, code)

class AddBookForm(BaseModel):
    tags: List[str] = list()
    pictures: List[str] = list()
    id: str
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

@app.post("/add_book")
async def seller_add_book(form: AddBookForm):
    code, msg = seller.add_book(**form.dict())
    return JSONResponse({"message": msg}, code)

class AddStockLevelForm(BaseModel):
    user_id: int
    book_id: str
    store_id: int
    add_stock_level: int

@app.post("/add_stock_level")
async def add_stock_level(form: AddStockLevelForm):
    code, msg = seller.add_stock_level(form.user_id, form.store_id, form.book_id, form.add_stock_level)
    return JSONResponse({"message": msg}, code)

class QueryStockLevelForm(BaseModel):
    user_id: int
    book_id: str
    store_id: int

@app.post("/query_stock_level")
async def query_stock_level(form: QueryStockLevelForm):
    code, msg = seller.query_stock_level(form.user_id, form.store_id, form.book_id)
    return JSONResponse({"message": msg}, code)

class ShippingForm(BaseModel):
    user_id: int
    seller_id: int
    book_id: str

@app.post("/shipping")
async def shipping(form: ShippingForm):
    code, msg = seller.shipping(
        form.user_id,
        form.seller_id,
        form.book_id
    )
    return JSONResponse({"message": msg}, code)

class ChangePriceForm(BaseModel):
    store_id: int
    book_id: str
    price: int

@app.post("/change_price")
async def change_price(form: ChangePriceForm):
    code, msg = seller.change_price(sid=form.store_id, bid=form.book_id, price=form.price)
    return JSONResponse({"message": msg}, code)

class QueryPriceForm(BaseModel):
    store_id: int
    book_id: str

@app.post("/query_price")
async def query_price(form: QueryPriceForm):
    code, msg = seller.query_price(sid=form.store_id, bid=form.book_id)
    return JSONResponse({"message": msg}, code)