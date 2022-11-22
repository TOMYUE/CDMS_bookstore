import requests
from urllib.parse import urljoin
from typing import *

class Auth:
    def __init__(self, url_prefix):
        self.url_prefix = urljoin(url_prefix, "auth/")

    def login(self, user_id: int, password: str, terminal: str) -> Tuple[int, str]:
        json = {"user_id": user_id, "password": password, "terminal": terminal}
        url = urljoin(self.url_prefix, "login")
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("token")

    def register_buyer(
        self,
        user_id: int,
        password: str,
        uname: str,
        account: str,
        balance: float
    ) -> int:
        json = {
            "user_id": user_id,
            "password": password,
            "user_name": uname,
            "account": account,
            "balance": balance
        }
        url = urljoin(self.url_prefix, "register")
        r = requests.post(url, json=json)
        return r.status_code

    def register_seller(
        self,
        user_id: int,
        store_id: int,
        password: str,
        uname: str,
        account: str,
        balance: float
    ) -> int:
        json = {
            "user_id": user_id,
            "store_id": store_id,
            "password": password,
            "user_name": uname,
            "account": account,
            "balance": balance
        }
        url = urljoin(self.url_prefix, "register")
        r = requests.post(url, json=json)
        return r.status_code

    def password(self, user_id: int, old_password: str, new_password: str) -> int:
        json = {
            "user_id": user_id,
            "oldPassword": old_password,
            "newPassword": new_password,
        }
        url = urljoin(self.url_prefix, "password")
        r = requests.post(url, json=json)
        return r.status_code

    def logout(self, user_id: int, token: str) -> int:
        json = {"user_id": user_id}
        headers = {"token": token}
        url = urljoin(self.url_prefix, "logout")
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def unregister(self, user_id: int, password: str) -> int:
        json = {"user_id": user_id, "password": password}
        url = urljoin(self.url_prefix, "unregister")
        r = requests.post(url, json=json)
        return r.status_code
