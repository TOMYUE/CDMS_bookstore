import pytest
import uuid
import random
from fe.access.new_buyer import register_new_buyer

from typing import *

class TestAddFunds:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.user_id = int(uuid.uuid1())
        self.password = str(self.user_id)
        self.uname = "test_add_funds_"
        self.account = "test_add_funds_account"
        self.balance = round(random.uniform(500, 1000), 6)
        self.buyer = register_new_buyer(self.user_id, self.password, self.uname, self.account, self.balance)
        yield

    def test_ok(self):
        code = self.buyer.add_funds(1000)
        assert code == 200

        code = self.buyer.add_funds(-1000)
        assert code == 200

    def test_error_user_id(self):
        self.buyer.user_id = self.buyer.user_id + "_x"
        code = self.buyer.add_funds(10)
        assert code != 200

    def test_error_password(self):
        self.buyer.password = self.buyer.password + "_x"
        code = self.buyer.add_funds(10)
        assert code != 200
