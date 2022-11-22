import random
import uuid

import pytest

from fe.access import auth
from fe import conf

from typing import *

class TestPassword:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.auth = auth.Auth(conf.URL)
        # register a user
        self.user_id = int(uuid.uuid1())
        self.old_password = "old_password_" + str(self.user_id)
        self.new_password = "new_password_" + str(self.user_id)
        self.uname = "test_pwd_" + str(self.user_id)
        self.account = "test_pwd_{}" + str(self.user_id)
        self.balance = round(random.uniform(1000, 10000), 6)
        self.terminal = "terminal_" + str(self.user_id)

        assert self.auth.register_buyer(self.user_id, self.old_password, self.uname, self.account, self.balance) == 200
        yield

    def test_ok(self):
        code = self.auth.password(self.user_id, self.old_password, self.new_password)
        assert code == 200

        code, new_token = self.auth.login(self.user_id, self.old_password, self.terminal)
        assert code != 200

        code, new_token = self.auth.login(self.user_id, self.new_password, self.terminal)
        assert code == 200

        code = self.auth.logout(self.user_id, new_token)
        assert code == 200

    def test_error_password(self):
        code = self.auth.password(self.user_id, self.old_password + "_x", self.new_password)
        assert code != 200

        code, new_token = self.auth.login(self.user_id, self.new_password, self.terminal)
        assert code != 200

    def test_error_user_id(self):
        code = self.auth.password(self.user_id, self.old_password, self.new_password)
        assert code != 200

        code, new_token = self.auth.login(self.user_id, self.new_password, self.terminal)
        assert code != 200
