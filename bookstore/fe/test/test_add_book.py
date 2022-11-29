import random

import pytest

from fe.access.new_seller import register_new_seller
from fe.access import book
import uuid
from typing import *


class TestAddBook:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        # do before test
        self.seller_id = int(uuid.uuid1())
        self.store_id = int(uuid.uuid1())
        self.uname = "test_add_book_stock_level1_store_{}".format(str(self.seller_id))
        self.password = self.seller_id
        self.account = "test_add_book_stock_level1_store"
        self.balance = round(random.uniform(500, 1000), 6)
        self.seller = register_new_seller(self.seller_id, self.store_id, self.password,
                                          self.uname, self.account, self.balance)

        code = self.seller.create_store(self.store_id)
        assert code == 200
        book_db = book.BookDB()
        self.books = book_db.get_book_info(0, 2) #TODO: related works with SQLORM

        yield
        # do after test

    def test_ok(self):
        for b in self.books:
            code = self.seller.add_book(self.store_id, 0, b)
            assert code == 200

    def test_error_non_exist_store_id(self):
        for b in self.books:
            # non exist store id
            code = self.seller.add_book(self.store_id, 0, b)
            assert code != 200

    def test_error_exist_book_id(self):
        for b in self.books:
            code = self.seller.add_book(self.store_id, 0, b)
            assert code == 200
        for b in self.books:
            # exist book id
            code = self.seller.add_book(self.store_id, 0, b)
            assert code != 200

    def test_error_non_exist_user_id(self):
        for b in self.books:
            # non exist user id
            self.seller.seller_id = self.seller.seller_id + "_x"
            code = self.seller.add_book(self.store_id, 0, b)
            assert code != 200

