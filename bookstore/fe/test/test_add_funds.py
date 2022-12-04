import pytest
import uuid
import random
from be.relations.seller import *
from be.relations.buyer import *
from be.relations.user import *
from typing import *


class TestAddFunds:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.user_id = None
        self.password = str(self.user_id)
        self.uname = "test_add_funds_"
        self.account = "test_add_funds_account"
        self.balance = round(random.uniform(500, 1000), 6)
        self.token = "test_add_funds"
        self.terminal = "terminal_{}".format(str(time.time()))

    def test_buyer_register(self):
        code, msg = buyer_register(self.uname, self.password,
                                   self.account, self.balance, self.token, self.terminal)
        assert code == 200

    def test_ok(self):
        code, msg = add_funds(1, self.password, 1000)
        assert code == 200

    def test_error_user_id(self):
        self.user_id = 999
        code = add_funds(self.user_id, self.password, 10)
        assert code != 200

    def test_error_password(self):
        self.password = self.password + "_x"
        code, msg = add_funds(1, self.password, 10)
        assert code != 200

    def test_renew(self):
        drop_all_table()
        create_table()
        copy_data_to_book(DBSession())
