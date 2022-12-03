import requests
from urllib.parse import urljoin
from typing import *


class Auth:
    def __init__(self, url_prefix):
        self.url_prefix = url_prefix

    def buyer_login(self, user_id: int, password: str, terminal: str) -> Tuple[int, str]:
        json = {"user_id": user_id, "password": password, "terminal": terminal}
        url = urljoin(self.url_prefix, "login")
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("token")

    def seller_login(self, user_id: int, password: str, terminal: str) -> Tuple[int, str]:
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
        url = urljoin(self.url_prefix, "buyer/register")
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
        url = urljoin(self.url_prefix, "seller/register")
        r = requests.post(url, json=json)
        return r.status_code

    def buyer_password(self, user_id: int, old_password: str, new_password: str) -> int:
        json = {
            "user_id": user_id,
            "oldPassword": old_password,
            "newPassword": new_password,
        }
        url = urljoin(self.url_prefix, "buyer/password")
        r = requests.post(url, json=json)
        return r.status_code

    def seller_password(self, user_id: int, old_password: str, new_password: str) -> int:
        json = {
            "user_id": user_id,
            "oldPassword": old_password,
            "newPassword": new_password,
        }
        url = urljoin(self.url_prefix, "seller/password")
        r = requests.post(url, json=json)
        return r.status_code

    def buyer_logout(self, user_id: int, token: str) -> int:
        json = {"user_id": user_id}
        headers = {"token": token}
        url = urljoin(self.url_prefix, "buyer/logout")
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def seller_logout(self, user_id: int, token: str) -> int:
        json = {"user_id": user_id}
        headers = {"token": token}
        url = urljoin(self.url_prefix, "seller/logout")
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def buyer_unregister(self, user_id: int, password: str) -> int:
        json = {"user_id": user_id, "password": password}
        url = urljoin(self.url_prefix, "buyer/unregister")
        r = requests.post(url, json=json)
        return r.status_code

    def seller_unregister(self, user_id: int, password: str) -> int:
        json = {"user_id": user_id, "password": password}
        url = urljoin(self.url_prefix, "seller/unregister")
        r = requests.post(url, json=json)
        return r.status_code