import time
import uuid
import random
import pytest

from fe.access import auth
from fe import conf
from typing import *


class TestLogin:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.auth = auth.Auth(conf.URL)
        # register a user
        self.user_id = int(uuid.uuid1())
        self.password = "password_" + str(self.user_id)
        self.uname = "test_login_" + str(self.user_id)
        self.account = "test_login_{}" + str(self.user_id)
        self.balance = round(random.uniform(1000, 10000), 6)
        self.terminal = "terminal_" + str(self.user_id)
        assert self.auth.register_buyer(self.user_id, self.password, self.uname, self.account, self.balance) == 200
        yield

    def test_ok(self):
        code, token = self.auth.login(self.user_id, self.password, self.terminal)
        assert code == 200

        code = self.auth.logout(self.user_id, token)
        assert code == 401

        code = self.auth.logout(self.user_id, token + "_x")
        assert code == 401

        code = self.auth.logout(self.user_id, token)
        assert code == 200

    def test_error_user_id(self):
        code, token = self.auth.login(self.user_id, self.password, self.terminal)
        assert code == 401

    def test_error_password(self):
        code, token = self.auth.login(self.user_id, self.password + "_x", self.terminal)
        assert code == 401
