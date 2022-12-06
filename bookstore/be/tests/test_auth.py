from fastapi.testclient import TestClient
from uuid import uuid1

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class SellerRequest:
    def __init__(self) -> None:
        print(sys.path)
        from run import app
        self.cli = TestClient(app)

    def register(self, expected_code=200) -> dict:
        json = {
            "user_id": int(uuid1()),
            "uname": str(uuid1()),
            "password": str(uuid1())
        }
        response = self.cli.post("/auth/seller/register", json=json)
        assert response.status_code == expected_code
        return json

    def login(self, user_id, uname, password, expected_code=200) -> dict:
        response = self.cli.post("/auth/seller/login")
        assert response.status_code == expected_code
        return {
            "user_id": user_id,
            "uname": uname,
            "password": password
        }

    def logout(self, ):
        raise Exception("TODO")

    def change_pwd():
        raise Exception("TODO")

# ************************************* write tests here, utilize seller request ************************************* #

def test_login_200():
    SellerRequest().register(200)