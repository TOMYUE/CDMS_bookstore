from uuid import uuid1

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tests.test_auth import AuthRequest
from typing import *

def rand_book():
    return {
        "id": str(uuid1()),
        "title": str(uuid1()),
        "author": str(uuid1()),
        "publisher": str(uuid1()), 
        "original_title": str(uuid1()), 
        "translator": str(uuid1()), 
        "pub_year": str(uuid1()), 
        "pages": int(uuid1()) % 1000, 
        "price": int(uuid1()) % 1000, 
        "binding": str(uuid1()), 
        "isbn": str(uuid1()), 
        "author_intro": str(uuid1()), 
        "book_intro": str(uuid1()), 
        "content": str(uuid1()), 
        "tags": [str(uuid1()) for i in range(20)],
        "pictures": [str(uuid1()) for i in range(20)],
    }

class SellerRequest(AuthRequest):
    def __init__(self) -> None:
        super().__init__()

    def create_rand_store(self, expected_code, user_id):
        store_id = int(uuid1()) % 1000
        self.create_store(expected_code, user_id, store_id)
        return {"sid": store_id}

    def create_store(self, expected_code, user_id, store_id):
        json = {
            "user_id": user_id,
            "store_id": store_id,
        }
        response = self.cli.post("/seller/create_store", json=json)
        assert response.status_code == expected_code, response.content

    def add_book(self, 
        expected_code, *,
        id: str,
        title: str,
        author: str,
        publisher: str, 
        original_title: str, 
        translator: str, 
        pub_year: str, 
        pages: int, 
        price: int, 
        binding: str, 
        isbn: str, 
        author_intro: str, 
        book_intro: str, 
        content: str, 
        tags: List[str] = list(),
        pictures: List[str] = list(),
    ):
        json = {
            "id": id,
            "title": title,
            "author": author,
            "publisher": publisher, 
            "original_title": original_title, 
            "translator": translator, 
            "pub_year": pub_year, 
            "pages": pages, 
            "price": price, 
            "binding": binding, 
            "isbn": isbn, 
            "author_intro": author_intro, 
            "book_intro": book_intro, 
            "content": content, 
            "tags": tags,
            "pictures": pictures,
        }
        response = self.cli.post("/seller/add_book", json=json)
        assert response.status_code == expected_code, response.content

    def add_rand_book(self, expected_code):
        book = rand_book()
        self.add_book(expected_code, **book)
        return book    

    def add_stock_level(self, 
        expected_code,
        user_id: int, 
        book_id: str, 
        store_id: int, 
        add_stock_level: int, 
    ):
        json = {
            "user_id": user_id,
            "book_id": book_id,
            "store_id": store_id,
            "add_stock_level": add_stock_level
        }
        response = self.cli.post("/seller/add_stock_level", json=json)
        assert response.status_code == expected_code, response.content

    def query_stock_level(self, 
        expected_code, 
        user_id: int,
        book_id: str,
        store_id: int
    ):
        json = {
            "user_id": user_id,
            "book_id": book_id,
            "store_id": store_id
        }
        response = self.cli.post("/seller/query_stock_level", json=json)
        assert response.status_code == expected_code, response.content
        return response.content

# ************************************* write test_* functions here, utilize these tools ************************************* #

def test_create_store_ok():
    seller = SellerRequest()
    seller_info = seller.seller_register(200)
    store_id = int(uuid1()) % 1000
    seller.create_store(200, seller_info["uid"], store_id)

def test_create_store_dup():
    seller = SellerRequest()
    seller_info = seller.seller_register(200)
    store_id = int(uuid1()) % 1000
    seller.create_store(200, seller_info["uid"], store_id)
    seller.create_store(500, seller_info["uid"], store_id)

def test_add_book():
    seller = SellerRequest()
    seller.add_book(200, **rand_book())

def test_add_stock_level():
    seller = SellerRequest()
    book = rand_book()
    seller.add_book(200, **book)
    seller_info = seller.seller_register()
    store_id = int(uuid1()) % 1000
    seller.create_store(200, seller_info["uid"], store_id)
    seller.add_stock_level(200, seller_info["uid"], book_id=str(book["id"]), store_id=store_id, add_stock_level=5)
    # raise Exception(seller.query_stock_level(200, seller_info["uid"], book_id=book["id"], store_id=store_id))
