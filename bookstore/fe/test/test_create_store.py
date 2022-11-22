import random

import pytest

from fe.access.new_seller import register_new_seller
import uuid

from typing import *

class TestCreateStore:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.user_id = int(uuid.uuid1())
        self.store_id = int(uuid.uuid1())
        self.password = self.user_id
        self.uname = "test_create_store_{}".format(str(self.user_id))
        self.account = "test_create_store"
        self.balance = round(random.uniform(500, 1000), 6)
        self.seller = register_new_seller(self.user_id, self.password, self.password,
                                          self.uname, self.account, self.balance)
        yield

    def test_ok(self):
        code = self.seller.create_store(self.store_id)
        assert code == 200

    def test_error_exist_store_id(self):
        code = self.seller.create_store(self.store_id)
        assert code == 200

        code = self.seller.create_store(self.store_id)
        assert code != 200
