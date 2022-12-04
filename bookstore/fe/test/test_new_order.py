import random

import pytest

# from fe.test.gen_book_data import GenBook
# # from fe.access.new_buyer import register_new_buyer
# # from fe.access.new_seller import register_new_seller
from be.relations.user import *
from be.relations.seller import *
import uuid

from typing import *


class TestNewOrder:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        # id of the seller, buyer and store
        self.seller_id = None
        self.buyer_id = None
        self.store_id = random.randint(1, 1000)
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
        # token and terminal of buyer and seller
        self.buyer_token = "test_new_order"
        self.buyer_terminal = "terminal_{}".format(str(time.time()))
        self.seller_token = "test_new_order"
        self.seller_terminal = "terminal_{}".format(str(time.time()))
        self.book = Book(bid="test_add",
                         title="test_add",
                         author="test",
                         publisher="test",
                         original_title="",
                         translator="",
                         pub_year="1999",
                         pages=512,
                         price=1024,
                         currency_unit="元",
                         binding="平装",
                         isbn="978754282382xxx",
                         author_intro="",
                         book_intro="",
                         content=""
                         )

    def test_buyer_register(self):
        code, msg = buyer_register(self.buyer_uname, self.buyer_password,
                                   self.buyer_account, self.buyer_balance, self.buyer_token, self.buyer_terminal)
        assert code == 200

    def test_seller_register(self):
        code, msg = seller_register(self.seller_uname, self.seller_password,
                                    self.seller_account, self.seller_balance, self.seller_token, self.seller_terminal)
        assert code == 200

    def test_seller_add_book(self):
        code, msg = add_book_to_store(self.seller_id, self.store_id, '1000067', 0)
        assert code == 200

    def test_non_exist_book_id(self):
        code, _, deal_id = new_order(1, 1, [("test_new_order_not_exist", 0)])
        print(deal_id)
        assert code != 200

    def test_low_stock_level(self):
        code, _, deal_id = new_order(1, 1, [('1000067', 10)])
        print(deal_id)
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

    def test_renew(self):
        drop_all_table()
        create_table()
        copy_data_to_book(DBSession())