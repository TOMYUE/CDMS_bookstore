from uuid import uuid1

import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tests.test_seller import SellerRequest, rand_book
from typing import *

class SearchRequest(SellerRequest):
    def __init__(self) -> None:
        super().__init__()

    def search_title(self, title, page, expected_code):
        json = {
            "title": title,
            "page": page
        }
        response = self.cli.post("/auth/search_title", json=json)
        assert response.status_code == expected_code, response.content
        return {}

    def search_title_in_store(self, title, page, sid, expected_code):
        json={
            "title": title,
            "page": page,
            "sid": sid
        }
        response = self.cli.post("/auth/search_title_in_store",json=json)
        assert response.status_code == expected_code, response.content
        return {}

    def search_tag(self, tag, page, expected_code):
        json={
            "tag": tag,
            "page": page
        }
        response = self.cli.post("/auth/search_tag", json=json)
        assert response.status_code == expected_code, response.content
        return {}

    def search_tag_in_store(self, tag, page, sid, expected_code):
        json={
            "tag": tag,
            "page": page,
            "sid": sid
        }
        response = self.cli.post("/auth/search_tag_in_store", json=json)
        assert response.status_code == expected_code, response.content
        return {}

    def search_content(self, book_intro, page, expected_code):
        json={
            "book_intro": book_intro,
            "page": page
        }
        response = self.cli.post("/auth/search_content", json=json)
        assert response.status_code == expected_code, response.content
        return {}

    def search_content_in_store(self, book_intro, page, sid, expected_code):
        json={
            "book_intro": book_intro,
            "page": page,
            "sid": sid
        }
        response = self.cli.post("/auth/search_content_in_store", json=json)
        assert response.status_code == expected_code, response.content
        return {}

    def search_author(self, author, page, expected_code):
        json = {
            "author": author,
            "page": page
        }
        response = self.cli.post("/auth/search_author", json=json)
        assert response.status_code == expected_code, response.content
        return {}

    def search_author_in_store(self, author, page, sid, expected_code):
        json = {
            "author": author,
            "page": page,
            "sid": sid
        }
        response = self.cli.post("/auth/search_author_in_store", json=json)
        assert response.status_code == expected_code, response.content
        return {}

# ************************************* write test_* functions here, utilize these tools ******************************#

def test_search():
    seller = SearchRequest()
    for i in range(5):
        book = rand_book()
        seller.add_book(200, **book)
        seller_info = seller.seller_register()
        store_id = int(uuid1())%1000
        seller.create_store(200, seller_info['uid'], store_id)
        seller.add_stock_level(200, seller_info["uid"], book_id=str(book["id"]), store_id=store_id, add_stock_level=5)

    # seller.search_title("我爱数据库",1,200)
    seller.search_title("",1,503)
    # seller.search_title_in_store(book['title'],1,store_id,200)
    seller.search_title_in_store("dontknow", 1, store_id, 503)
    seller.search_title_in_store(book['title'], 1, 0, 506)

    # seller.search_tag(book['tags'][0], 1, 200)
    seller.search_tag("dontknow", 1, 504)
    # seller.search_tag_in_store(book['tags'][0], 1, store_id, 200)
    seller.search_tag_in_store("dontknow", 1, store_id, 504)
    seller.search_tag_in_store(book['tags'][0], 1, 0, 506)

    seg = (book['book_intro'][0:2])
    # seller.search_content(seg, 1, 200)
    seller.search_content("dontknow", 1, 505)
    # seller.search_content_in_store(book['book_intro'][0:2], 1, store_id, 200)
    seller.search_content_in_store(book['book_intro'][0:2], 1, 0, 506)
    seller.search_content_in_store("book", 1, store_id, 505)

    # seller.search_author(book['author'], 1, 200)
    seller.search_author("nobody", 1, 507)
    # seller.search_author_in_store(book['author'], 1, store_id, 200)
    seller.search_author_in_store("nobody", 1,store_id, 507)
    seller.search_author_in_store(book['author'], 1, 0, 506)
