import random
import time
import uuid
import pytest

from fe.access import auth
from fe import conf
from be.relations.seller import *
from be.relations.buyer import *
from be.relations.user import *
from typing import *

class TestRegister:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.auth = auth.Auth(conf.URL)
        self.user_id = int(uuid.uuid1())
        self.uname = "test_register1"
        self.password = "test_register_1"
        self.account = "test_register_" + str(self.user_id)
        self.balance = round(random.uniform(1000, 10000), 6)
        self.token = "token"
        self.terminal = "terminal_{}".format(str(time.time()))
        yield

    def test_buyer_register(self):
        code, msg = buyer_register(self.uname, self.password,self.account, self.balance, self.token, self.terminal)
        assert code == 200

    def test_seller_register(self):
        code, msg = seller_register(self.uname, self.password,self.account, self.balance, self.token, self.terminal)
        assert code == 200

    #user exists already
    def test_buyer_register_error(self):
        code, msg = buyer_register(self.uname, "newpassword",self.account, self.balance, self.token, self.terminal)
        assert code == 512

    #user exists already
    def test_seller_register_error(self):
        code, msg = seller_register(self.uname, "newpassword",self.account, self.balance, self.token, self.terminal)
        assert code == 512
    def test_seller_login_ok(self):
        code, msg, token = seller_login(self.uname, self.password, self.terminal)
        print(msg)
        assert code == 200

    #user not exist
    def test_seller_login_error1(self):
        code, msg, token = seller_login("nobody", self.password, self.terminal)
        assert code == 511

    #input wrong password
    def test_seller_login_error2(self):
        code, msg, token = seller_login(self.uname, "self.password", self.terminal)
        print(msg)
        assert code == 401

    def test_buyer_login_ok(self):
        code, msg, token = buyer_login(self.uname, self.password, self.terminal)
        print(msg)
        assert code == 200

    # user not exist
    def test_buyer_login_error1(self):
        code, msg, token = buyer_login("nobody", self.password, self.terminal)
        assert code == 511

    # input wrong password
    def test_buyer_login_error2(self):
        # print(self.password)
        code, msg, token = buyer_login(self.uname, "self.password", self.terminal)
        print(msg)
        assert code == 401

    def test_seller_logout_ok(self):
        code, msg = seller_logout(self.uname, self.token)
        assert code == 200

    #error token
    def test_seller_logout_error(self):
        code, msg = seller_logout(self.uname,"unknown")
        assert code == 401

    def test_buyer_logout_ok(self):
        code, msg = buyer_logout(self.uname, self.token)
        assert code == 200

    #error token
    def test_buyer_logout_error(self):
        code, msg = buyer_logout(self.uname,"unknown")
        assert code == 401

    #user none exists
    def test_seller_change_pwd_error1(self):
        code, msg = seller_change_password("nobody", self.password, "test_register_2")
        assert code == 511
    #wrong password
    def test_seller_change_pwd_error2(self):
        code, msg = seller_change_password(self.uname, "mima", "test_register_2")
        assert code == 401

    def test_seller_change_pwd_ok(self):
        code, msg = seller_change_password(self.uname, self.password,"test_register_1")
        assert code == 200

    # user none exists
    def test_buyer_change_pwd_error1(self):
        code, msg = buyer_change_password("nobody", self.password, "test_register_2")
        assert code == 511

    # wrong password
    def test_buyer_change_pwd_error2(self):
        code, msg = buyer_change_password(self.uname, "mima", "test_register_2")
        assert code == 401

    def test_buyer_change_pwd_ok(self):
        code, msg = buyer_change_password(self.uname, self.password, "test_register_1")
        assert code == 200

    # user none exists
    def test_seller_unregister_error1(self):
        code, msg = seller_unregister("nobody", self.password)
        assert code == 511

    # wrong password
    def test_seller_unregister_error2(self):
        code, msg = seller_unregister(self.uname, "mima")



    def test_seller_unregister_ok(self):
        code, msg = seller_unregister(self.uname, self.password)
        assert code == 200
    # user none exists
    def test_buyer_unregister_error1(self):
        code, msg = buyer_unregister("nobody", self.password)
        assert code == 511

    # wrong password
    def test_buyer_unregister_error2(self):
        code, msg = buyer_unregister(self.uname, "mima")
        assert code == 401

    def test_buyer_unregister_ok(self):
        code, msg = buyer_unregister(self.uname, self.password)
        assert code == 200
    # def test_unregister_ok(self):
    #     code = self.auth.register_buyer(self.user_id, self.password, self.uname, self.account, self.balance)
    #     assert code == 200
    #
    #     code = self.auth.buyer_unregister(self.user_id, self.password)
    #     assert code == 200

    # def test_unregister_error_authorization(self):
    #     code = self.auth.register_buyer(self.user_id, self.password, self.uname, self.account, self.balance)
    #     assert code == 200
    #
    #     code = self.auth.buyer_unregister(self.user_id, self.password)
    #     assert code != 200
    #
    #     code = self.auth.buyer_unregister(self.user_id, self.password + "_x")
    #     assert code != 200
    #
    # def test_register_error_exist_user_id(self):
    #     code = self.auth.register_buyer(self.user_id, self.password, self.uname, self.account, self.balance)
    #     assert code == 200
    #
    #     code = self.auth.register_buyer(self.user_id, self.password, self.uname, self.account, self.balance)
    #     assert code != 200
