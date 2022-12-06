from fastapi.testclient import TestClient
from uuid import uuid1

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class AuthRequest:
    def __init__(self) -> None:
        print(sys.path)
        from run import app
        self.cli = TestClient(app)

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
        assert response.status_code == expected_code
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
        assert response.status_code == expected_code
        return json

    def seller_login(self, uname, password, terminal,expected_code=200) -> dict:
        json = {
            "uname":uname,
            "password": password,
            "terminal": terminal
        }
        response = self.cli.post("/auth/seller/login",json=json)
        assert response.status_code == expected_code
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
        assert response.status_code == expected_code
        return {
            "uname": uname,
            "password": password
        }

    def logout(self):
        raise Exception("TODO")

    def change_pwd(self):
        raise Exception("TODO")


# ************************************* write test_* functions here, utilize these tools ************************************* #

def test_seller_register_ok():
    AuthRequest().seller_register(200)

def test_buyer_register_ok():
    AuthRequest().buyer_register(200)

def test_seller_login_ok():
    data = AuthRequest().seller_register(200)
    AuthRequest().seller_login(data["uname"], data["password"],data["terminal"],200)

def test_buyer_login_ok():
    data = AuthRequest().buyer_register(200)
    AuthRequest().buyer_login(data["uname"], data["password"],data["terminal"],200)
