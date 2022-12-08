from uuid import uuid1

import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
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
        return response.json()

    def search_title(self, title, page, expected_code):
        json = {
            "title": title,
            "page": page
        }
        response = self.cli.post("/auth/search_title", json=json)
        assert response.status_code == expected_code
        return {}

    def search_title_in_store(self, title, page, sid, expected_code):
        json={
            "title": title,
            "page": page,
            "sid": sid
        }
        response = self.cli.post("/auth/search_title_in_store",json=json)
        assert response.status_code == expected_code
        return {}

    def search_tag(self, tag, page, expected_code):
        json={
            "tag": tag,
            "page": page
        }
        response = self.cli.post("/auth/search_tag", json=json)
        assert response.status_code == expected_code
        return {}

    def search_tag_in_store(self, tag, page, sid, expected_code):
        json={
            "tag": tag,
            "page": page,
            "sid": sid
        }
        response = self.cli.post("/auth/search_tag_in_store", json=json)
        assert response.status_code == expected_code
        return {}

    def search_content(self, book_intro, page, expected_code):
        json={
            "book_intro": book_intro,
            "page": page
        }
        response = self.cli.post("/auth/search_content", json=json)
        assert response.status_code == expected_code
        return {}

    def search_content_in_store(self, book_intro, page, sid, expected_code):
        json={
            "book_intro": book_intro,
            "page": page,
            "sid": sid
        }
        response = self.cli.post("/auth/search_content_in_store", json=json)
        assert response.status_code == expected_code
        return {}

    def search_author(self, author, page, expected_code):
        json = {
            "author": author,
            "page": page
        }
        response = self.cli.post("/auth/search_author", json=json)
        assert response.status_code == expected_code
        return {}

    def search_author_in_store(self, author, page, sid, expected_code):
        json = {
            "author": author,
            "page": page,
            "sid": sid
        }
        response = self.cli.post("/auth/search_author_in_store", json=json)
        assert response.status_code == expected_code
        return {}
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
    assert seller.query_stock_level(200, seller_info["uid"], book_id=book["id"], store_id=store_id)["message"] == 5

def test_search():
    seller = SellerRequest()
    for i in range(5):
        book = rand_book()
        seller.add_book(200, **book)
        seller_info = seller.seller_register()
        store_id = int(uuid1())%1000
        seller.create_store(200, seller_info['uid'], store_id)
        seller.add_stock_level(200, seller_info["uid"], book_id=str(book["id"]), store_id=store_id, add_stock_level=5)
    seller.search_title(book['title'],1,200)
    seller.search_title("",1,503)
    seller.search_title_in_store(book['title'],1,store_id,200)
    seller.search_title_in_store("dontknow", 1, store_id, 503)
    seller.search_title_in_store(book['title'], 1, 0, 506)

    seller.search_tag(book['tags'][0], 1, 200)
    seller.search_tag("dontknow", 1, 504)
    seller.search_tag_in_store(book['tags'][0], 1, store_id, 200)
    seller.search_tag_in_store("dontknow", 1, store_id, 504)
    seller.search_tag_in_store(book['tags'][0], 1, 0, 506)

    seg = (book['book_intro'][0:2])
    seller.search_content(seg, 1, 200)
    seller.search_content("dontknow", 1, 505)
    seller.search_content_in_store(book['book_intro'][0:2], 1, store_id, 200)
    seller.search_content_in_store(book['book_intro'][0:2], 1, 0, 506)
    seller.search_content_in_store("book", 1, store_id, 505)

    seller.search_author(book['author'], 1, 200)
    seller.search_author("nobody", 1, 507)
    seller.search_author_in_store(book['author'], 1, store_id, 200)
    seller.search_author_in_store("nobody", 1,store_id, 507)
    seller.search_author_in_store(book['author'], 1, 0, 506)
