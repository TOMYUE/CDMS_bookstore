import random

import pytest

from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.new_seller import register_new_seller
import uuid

from typing import *


class TestNewOrder:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        # id of the seller, buyer and store
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
        self.buyer_balance =  round(random.uniform(500, 1500), 6)
        self.seller_balance = round(random.uniform(500, 1500), 6)

        self.buyer = register_new_buyer(self.buyer_id, self.buyer_password,
                                        self.buyer_uname, self.buyer_account, self.buyer_balance)
        self.seller = register_new_seller(self.seller_id, self.seller_password,
                                          self.seller_uname, self.seller_account, self.seller_balance)
        self.gen_book = GenBook(self.seller_id, self.store_id)
        yield

    def test_non_exist_book_id(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=True, low_stock_level=False)
        assert ok
        code, _ = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code != 200

    def test_low_stock_level(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=True)
        assert ok
        code, _ = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code != 200

    def test_ok(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, _ = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200

    def test_non_exist_user_id(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        self.buyer.user_id = self.buyer.user_id + "_x"
        code, _ = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code != 200

    def test_non_exist_store_id(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, _ = self.buyer.new_order(-self.store_id, buy_book_id_list)
        assert code != 200
