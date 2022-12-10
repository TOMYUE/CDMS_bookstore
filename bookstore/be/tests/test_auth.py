from fastapi.testclient import TestClient
from uuid import uuid1

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class AuthRequest:
    def __init__(self) -> None:
        from run import app
        self.cli = TestClient(app())

    def seller_register(self, expected_code=200) -> dict:
        json = {
            "uname": str(uuid1()),
            "password": str(uuid1()),
            "account": str(uuid1()),
            "balance": 0.0,
            "token": str(uuid1()),
            "terminal": str(uuid1())
        }
        response = self.cli.post("/auth/seller/register", json=json)
        assert response.status_code == expected_code, response.content
        res = response.json()
        json.update({"uid": res['uid']})
        return json

    def buyer_register(self, expected_code=200) -> dict:
        json = {
            "uname": str(uuid1()),
            "password": str(uuid1()),
            "account": str(uuid1()),
            "balance": float(0.0),
            "token": str(uuid1()),
            "terminal": str(uuid1())
        }
        response = self.cli.post("/auth/buyer/register", json=json)
        assert response.status_code == expected_code, response.content
        res = response.json()
        json.update({"uid": res['uid']})
        return json

    def seller_login(self, uname, password, terminal,expected_code=200) -> dict:
        json = {
            "uname":uname,
            "password": password,
            "terminal": terminal
        }
        response = self.cli.post("/auth/seller/login",json=json)
        assert response.status_code == expected_code, response.content
        return {
            "uname": uname,
            "password": password
        }

    def buyer_login(self, uname, password, terminal,expected_code=200) -> dict:
        json = {
            "uname":uname,
            "password": password,
            "terminal": terminal
        }
        response = self.cli.post("/auth/buyer/login",json=json)
        assert response.status_code == expected_code, response.content
        return {
            "uname": uname,
            "password": password
        }


    def seller_logout(self,uname, token, expected_code=200):
        json={
                "uname":uname,
                "token":token
        }
        response = self.cli.post("/auth/seller/logout",json=json)
        assert response.status_code == expected_code, response.content
        return {}

    def buyer_logout(self,uname, token, expected_code=200):
        json={
                "uname":uname,
                "token":token
        }
        response = self.cli.post("/auth/buyer/logout",json=json)
        assert response.status_code == expected_code, response.content
        return {}

    def seller_ungister(self, uname, pwd, expected_code=200):
        json={
            "uname":uname,
            "password":pwd
        }
        response= self.cli.post("/auth/seller/unregister",json=json)
        assert response.status_code == expected_code, response.content
        return {}

    def buyer_ungister(self, uname, pwd, expected_code=200):
        json={
            "uname":uname,
            "password":pwd
        }
        response= self.cli.post("/auth/buyer/unregister",json=json)
        assert response.status_code == expected_code, response.content
        return {}

    def seller_change_pwd(self, uname,old_password, new_password, expected_code):
        json={
            "uname":uname,
            "old_password":old_password,
            "new_password":new_password
        }
        response = self.cli.post("/auth/seller/password",json=json)
        assert response.status_code == expected_code, response.content
        return {}

    def buyer_change_pwd(self, uname,old_password, new_password, expected_code):
        json={
            "uname":uname,
            "old_password":old_password,
            "new_password":new_password
        }
        response = self.cli.post("/auth/buyer/password",json=json)
        assert response.status_code == expected_code, response.content
        return {}

# ************************************* write test_* functions here, utilize these tools ************************************* #

def test_seller_register_ok():
    auth = AuthRequest()
    auth.seller_register(200)

def test_buyer_register_ok():
    auth = AuthRequest()
    auth.buyer_register(200)

def test_seller_login_ok():
    auth = AuthRequest()
    data = auth.seller_register(200)
    auth.seller_login(data["uname"], data["password"],data["terminal"],200)

#input wrong password
def test_seller_login_error1():
    auth = AuthRequest()
    data = auth.seller_register(200)
    auth.seller_login(data["uname"], "password", data["terminal"],501)

#user not exists
def test_seller_login_error2():
    auth = AuthRequest()
    data = auth.seller_register(200)
    auth.seller_login("nobody", "password", data["terminal"],502)


def test_buyer_login_ok():
    auth = AuthRequest()
    data = auth.buyer_register(200)
    auth.buyer_login(data["uname"], data["password"],data["terminal"],200)

#input wrong password
def test_buyer_login_error1():
    auth = AuthRequest()
    data = auth.buyer_register(200)
    auth.buyer_login(data["uname"], "password", data["terminal"],501)

#user not exists
def test_buyer_login_error2():
    auth = AuthRequest()
    data = auth.buyer_register(200)
    auth.buyer_login("nobody", "password", data["terminal"],502)


# def test_seller_logout_ok():
def test_seller_logout_ok():
    auth = AuthRequest()
    data = auth.seller_register(200)
    auth.seller_logout(data['uname'], data['token'],200)

#wrong token
def test_seller_logout_error():
    auth = AuthRequest()
    data = auth.seller_register(200)
    auth.seller_logout(data['uname'], "faketoken",501)

# def test_seller_logout_ok():
def test_buyer_logout_ok():
    auth = AuthRequest()
    data = auth.buyer_register(200)
    auth.buyer_logout(data['uname'], data['token'], 200)

# wrong token
def test_buyer_logout_error():
    auth = AuthRequest()
    data = auth.buyer_register(200)
    auth.buyer_logout(data['uname'], "faketoken", 501)

def test_seller_unregister_ok():
    auth = AuthRequest()
    data = auth.seller_register(200)
    auth.seller_ungister(data['uname'],data['password'],200)

#input wrong password
def test_seller_unregister_error1():
    auth = AuthRequest()
    data = auth.seller_register(200)
    auth.seller_ungister(data['uname'],"fakepassword",501)

#user none exists
def test_seller_unregister_error2():
    auth = AuthRequest()
    data = auth.seller_register(200)
    auth.seller_ungister("nobody","fakepassword",502)

def test_buyer_unregister_ok():
    auth = AuthRequest()
    data = auth.buyer_register(200)
    auth.buyer_ungister(data['uname'], data['password'], 200)

# input wrong password
def test_buyer_unregister_error1():
    auth = AuthRequest()
    data = auth.buyer_register(200)
    auth.buyer_ungister(data['uname'], "fakepassword", 501)

# user none exists
def test_buyer_unregister_error2():
    auth = AuthRequest()
    data = auth.buyer_register(200)
    auth.buyer_ungister("nobody", "fakepassword", 502)

def test_seller_change_pwd_ok():
    auth = AuthRequest()
    data = auth.seller_register(200)
    auth.seller_change_pwd(data['uname'],data['password'],data['password'],200)

#input wrong password
def test_seller_change_pwd_error1():
    auth = AuthRequest()
    data = auth.seller_register(200)
    auth.seller_change_pwd(data['uname'],"fakepassword",data['password'],501)

#user none exists
def test_seller_change_pwd_error2():
    auth = AuthRequest()
    data = auth.seller_register(200)
    auth.seller_change_pwd("nobody",data['password'],data['password'],502)


def test_buyer_change_pwd_ok():
    auth = AuthRequest()
    data = auth.buyer_register(200)
    auth.buyer_change_pwd(data['uname'],data['password'],data['password'],200)

#input wrong password
def test_buyer_change_pwd_error1():
    auth = AuthRequest()
    data = auth.buyer_register(200)
    auth.buyer_change_pwd(data['uname'],"fakepassword",data['password'],501)

#user none exists
def test_buyer_change_pwd_error2():
    auth = AuthRequest()
    data = auth.buyer_register(200)
    auth.buyer_change_pwd("nobody",data['password'],data['password'],502)

