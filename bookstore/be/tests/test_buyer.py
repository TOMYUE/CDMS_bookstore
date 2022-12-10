import random

from fastapi.testclient import TestClient
from relations.init import drop_all_table, create_table, copy_data_to_book, db_session, Store
from test_seller import SellerRequest, rand_book
from test_auth import AuthRequest
from uuid import uuid1

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class BuyerRequest:
    def __init__(self):
        from run import app
        self.cli = TestClient(app())

    def new_order(self, expected_code, buyer_id, store_id, book_id, quantity):
        json = {
            "user_id": buyer_id,
            "store_id": store_id,
            "id_and_num": [(book_id, quantity)]
        }
        response = self.cli.post("/buyer/new_order", json=json)
        print(response.json())
        assert response.status_code == expected_code

    def payment(self, expected_code, buyer_id, store_id):
        json = {
            "user_id": buyer_id,
            "store_id": store_id
        }
        response = self.cli.post("/buyer/payment", json=json)
        assert response.status_code == expected_code
        return json

    def add_funds(self, expected_code, value, buyer_id):
        json = {
            "user_id": buyer_id,
            "add_value": value
        }
        response = self.cli.post("/buyer/add_funds", json=json)
        assert response.status_code == expected_code
        return json

    def receive_book(self, expected_code, buyer_id, store_id, deal_id):
        json = {
            "user_id": buyer_id,
            "store_id": store_id,
            "deal_id": deal_id
        }
        response = self.cli.post("/buyer/receive_book", json=json)
        assert response.status_code == expected_code
        return json

    def history(self, expected_code, buyer_id):
        json = {
            "user_id": buyer_id
        }
        response = self.cli.post("/buyer/history", json=json)
        assert response.status_code == expected_code
        return json

    def cancel_deal(self, expected_code, buyer_id, deal_id):
        json = {
            "user_id": buyer_id,
            "deal_id": deal_id
        }
        response = self.cli.post("/buyer/cancel_deal", json=json)
        assert response.status_code == expected_code, response.content
        return json


# ************************************* write test_* functions here, utilize these tools ******************************#


def test_initialization():
    seller = SellerRequest()
    book = rand_book()
    seller.add_book(200, **book)
    seller_info = seller.seller_register()
    store_id = int(uuid1()) % 1000
    seller.create_store(200, seller_info["uid"], store_id)
    seller.add_stock_level(200, seller_info["uid"], book_id=str(book["id"]), store_id=store_id, add_stock_level=5)


def test_new_order():
    auth = AuthRequest()
    buyer = BuyerRequest()
    seller = SellerRequest()
    book_id = '1000167'
    add_stock_level = 5
    buyer_info = auth.buyer_register(200)
    seller_info = auth.seller_register(200)
    store_id = int(uuid1()) % 1000
    seller.create_store(200, seller_info["uid"], store_id)
    seller.add_stock_level(200, seller_info["uid"], book_id, store_id, add_stock_level)
    buyer.new_order(200, buyer_info['uid'], store_id, book_id, 1)


def test_payment():
    auth = AuthRequest()
    buyer = BuyerRequest()
    seller = SellerRequest()
    buyer_info = auth.buyer_register(200)
    book_id = '1000167'
    add_stock_level = 5
    seller_info = auth.seller_register(200)
    store_id = int(uuid1()) % 1000
    seller.create_store(200, seller_info["uid"], store_id)
    seller.add_stock_level(200, seller_info["uid"], book_id, store_id, add_stock_level)
    buyer.payment(200, buyer_info['uid'], store_id)


def test_add_funds():
    auth = AuthRequest()
    buyer = BuyerRequest()
    buyer_info = auth.buyer_register(200)
    print("xxxxxxxxxxxxxxxx")
    print(buyer_info['uid'])
    print("xxxxxxxxxxxxxxxx")
    buyer.add_funds(200, 101, buyer_info['uid'])


def test_receive_book():
    auth = AuthRequest()
    buyer = BuyerRequest()
    seller = SellerRequest()
    book_id = '1000167'
    add_stock_level = 5
    buyer_info = auth.buyer_register(200)
    seller_info = auth.seller_register(200)
    store_id = int(uuid1()) % 1000
    seller.create_store(200, seller_info["uid"], store_id)
    seller.add_stock_level(200, seller_info["uid"], book_id, store_id, add_stock_level)
    buyer.new_order(200, buyer_info['uid'], store_id, book_id, 1)
    buyer.receive_book(200, buyer_info['uid'], store_id, 1)

def test_history():
    auth = AuthRequest()
    buyer = BuyerRequest()
    seller = SellerRequest()
    book_id = '1000167'
    add_stock_level = 5
    buyer_info = auth.buyer_register(200)
    seller_info = auth.seller_register(200)
    store_id = int(uuid1()) % 1000
    seller.create_store(200, seller_info["uid"], store_id)
    seller.add_stock_level(200, seller_info["uid"], book_id, store_id, add_stock_level)
    buyer.new_order(200, buyer_info['uid'], store_id, book_id, 1)
    buyer.history(200, buyer_info['uid'])


def test_cancel_deal():
    auth = AuthRequest()
    buyer = BuyerRequest()
    seller = SellerRequest()
    book_id = '1000167'
    add_stock_level = 5
    buyer_info = auth.buyer_register(200)
    seller_info = auth.seller_register(200)
    store_id = int(uuid1()) % 1000
    seller.create_store(200, seller_info["uid"], store_id)
    seller.add_stock_level(200, seller_info["uid"], book_id, store_id, add_stock_level)
    buyer.new_order(200, buyer_info['uid'], store_id, book_id, 1)
    buyer.cancel_deal(200, buyer_info['uid'], 1)
