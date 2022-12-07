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
        self.cli = TestClient(app)
        self.seller_id = None
        self.buyer_id = None
        self.seller_name = "test_seller"
        self.buyer_name = "test_buyer"
        self.seller_pwd = str(uuid1())
        self.buyer_pwd = str(uuid1())
        self.seller_account = "test_seller_account"
        self.buyer_account = "test_buyer_account"
        self.seller_token = "test_seller_token"
        self.buyer_token = "test_buyer_token"
        self.seller_terminal = "test_seller_ter_"
        self.buyer_terminal = "test_buyer_ter_"
        self.store_id = random.randint(1000, 9999)
        self.deal_id = None

    def new_order(self, expected_code, buyer_id, store_id, book_id, quantity):
        json = {
            "user_id": buyer_id,
            "store_id": store_id,
            "id_and_num": [(book_id, quantity)]
        }
        response = self.cli.post("/buyer/new_order", json=json)
        assert response.status_code == expected_code
        self.deal_id = response.json()['deal_id']
        return json

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
            "sid": store_id,
            "did": deal_id
        }
        response = self.cli.post("/buyer/receive_book", json=json)
        assert response.status_code == expected_code
        return json

    def history(self, expected_code):
        json = {
            "uid": self.buyer_id
        }
        response = self.cli.post("/buyer/history", json=json)
        assert response.status_code == expected_code
        return json

    def cancel_deal(self, expected_code):
        json = {
            "uid": self.buyer_id,
            "did": self.deal_id
        }
        response = self.cli.post("/buyer/cancel_deal", json=json)
        assert response.status_code == expected_code
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
    buyer.new_order(200, buyer_info['uid'], store_id, book_id, add_stock_level)


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
    buyer.add_funds(200, buyer_info['uid'], 100)


def test_receive_book():
    auth = AuthRequest()
    # buyer register
    buyer = BuyerRequest()
    buyer_info = auth.buyer_register(200)
    # seller register
    seller = SellerRequest()
    seller_info = auth.seller_register(200)
    store_id = int(uuid1()) % 1000
    book_id = '1000167'
    add_stock_level = 10
    seller.create_store(200, seller_info["uid"], store_id)
    seller.add_stock_level(200, seller_info["uid"], book_id, store_id, add_stock_level)
    # buyer buy a book, get a deal id
    buyer.receive_book(200, buyer_info['uid'], )

# def test_history():
#
#
# def test_cancel_deal():

