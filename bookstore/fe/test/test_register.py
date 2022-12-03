import random
import time
import uuid
import pytest

from fe.access import auth
from fe import conf

from typing import *

class TestRegister:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.auth = auth.Auth(conf.URL)
        self.user_id = int(uuid.uuid1())
        self.uname = "test_register"
        self.password = "test_register_" + str(self.user_id)
        self.account = "test_register_" + str(self.user_id)
        self.balance = round(random.uniform(1000, 10000), 6)
        yield

    def test_register_ok(self):
        code = self.auth.register_buyer(self.user_id, self.password, self.uname, self.account, self.balance)
        assert code == 200

    def test_unregister_ok(self):
        code = self.auth.register_buyer(self.user_id, self.password, self.uname, self.account, self.balance)
        assert code == 200

        code = self.auth.buyer_unregister(self.user_id, self.password)
        assert code == 200

    def test_unregister_error_authorization(self):
        code = self.auth.register_buyer(self.user_id, self.password, self.uname, self.account, self.balance)
        assert code == 200

        code = self.auth.buyer_unregister(self.user_id, self.password)
        assert code != 200

        code = self.auth.buyer_unregister(self.user_id, self.password + "_x")
        assert code != 200

    def test_register_error_exist_user_id(self):
        code = self.auth.register_buyer(self.user_id, self.password, self.uname, self.account, self.balance)
        assert code == 200

        code = self.auth.register_buyer(self.user_id, self.password, self.uname, self.account, self.balance)
        assert code != 200
