import random

import pytest

from fe.access.buyer import Buyer
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
import uuid

from typing import *


class TestPayment:
    seller_id: int
    store_id: int
    buyer_id: int
    password: str
    buy_book_info_list: [Book]
    total_price: int
    order_id: str
    buyer: Buyer

    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        # initialization of the seller and buyer
        self.seller_id = int(uuid.uuid1())
        self.buyer_id = int(uuid.uuid1())
        self.store_id = int(uuid.uuid1())
        # pwd of the buyer and seller
        self.buyer_password = "test_new_order_buyer_" + str(self.buyer_id)
        self.seller_password = "test_new_order_seller_" + str(self.seller_id)
        # uname of the buyer and seller
        self.buyer_uname = "test_new_order_buyer_" + str(self.buyer_id)
        self.seller_uname = "test_new_order_seller_" + str(self.seller_id)
        # account of the buyer and seller
        self.buyer_account = "test_new_order_buyer_" + str(self.buyer_id)
        self.seller_account = "test_new_order_seller_" + str(self.seller_id)
        # balance of the buyer and seller
        self.buyer_balance = round(random.uniform(1000, 1500), 6)
        self.seller_balance = round(random.uniform(1000, 1500), 6)
        # initialization of book related info
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.buyer_password, self.buyer_uname, self.buyer_account, self.buyer_balance)
        self.buyer = b
        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        self.total_price = 0
        for item in self.buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num
        yield

    def test_ok(self):
        code = self.buyer.add_funds(self.total_price)
        assert code == 200
        code = self.buyer.payment(self.order_id)
        assert code == 200

    def test_authorization_error(self):
        code = self.buyer.add_funds(self.total_price)
        assert code == 200
        self.buyer.password = self.buyer.password + "_x"
        code = self.buyer.payment(self.order_id)
        assert code != 200

    def test_not_suff_funds(self):
        code = self.buyer.add_funds(self.total_price - 1)
        assert code == 200
        code = self.buyer.payment(self.order_id)
        assert code != 200

    def test_repeat_pay(self):
        code = self.buyer.add_funds(self.total_price)
        assert code == 200
        code = self.buyer.payment(self.order_id)
        assert code == 200

        code = self.buyer.payment(self.order_id)
        assert code != 200
