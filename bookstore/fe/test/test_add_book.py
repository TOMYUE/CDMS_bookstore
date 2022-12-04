import random
import pytest
from be.relations.seller import *
from be.relations.user import seller_register
import uuid
from typing import *


class TestAddBook:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        # do before test
        self.seller = None
        self.store = None
        self.seller_id = None
        self.store_id = random.randint(1, 1000)
        self.uname = "test_add_book_{}"
        self.password = str(time.time())
        self.account = "test_add_book_"
        self.balance = round(random.uniform(500, 1000), 6)
        self.stock_level = 10
        self.token = "test_add_book"
        self.terminal = "terminal_{}".format(str(time.time()))
        self.book = Book(bid="test_add",
                         title="test_add",
                         author="test",
                         publisher="test",
                         original_title="",
                         translator="",
                         pub_year="1999",
                         pages=512,
                         price=1024,
                         currency_unit="元",
                         binding="平装",
                         isbn="978754282382xxx",
                         author_intro="",
                         book_intro="",
                         content=""
                         )

    def test_seller_register(self):
        code, msg = seller_register(self.uname, self.password,
                                    self.account, self.balance, self.token, self.terminal)
        # self.seller_id = uid
        assert code == 200
        # assert self.seller_id is not None


    # do after test
    def test_ok(self):
        code, msg = add_book(1, self.store_id, self.stock_level,
                        id="test_add",
                        title="test_add",
                        author = "test",
                        publisher = "test",
                        original_title = "",
                        translator = "",
                        pub_year = "1999",
                        pages = 512,
                        price = 1024,
                        binding = "平装",
                        isbn = "978754282382xxx",
                        author_intro = "",
                        book_intro = "",
                        content = "")
        assert code == 200

    def test_error_non_exist_store_id(self):
        code = add_book(self.seller_id, "None exist", self.stock_level,
                        id="test_add",
                        title="test_add",
                        author="test",
                        publisher="test",
                        original_title="",
                        translator="",
                        pub_year="1999",
                        pages=512,
                        price=1024,
                        binding="平装",
                        isbn="978754282382xxx",
                        author_intro="",
                        book_intro="",
                        content="")
        rm_book_sql = '''delete from "Book" where bid='test_add';'''
        with db_session() as session:
            session.execute(rm_book_sql)
            session.commit()
        assert code != 200

    def test_error_non_exist_user_id(self):
        code = add_book("None exist", self.store_id, self.stock_level,
                        id="test_add",
                        title="test_add",
                        author="test",
                        publisher="test",
                        original_title="",
                        translator="",
                        pub_year="1999",
                        pages=512,
                        price=1024,
                        binding="平装",
                        isbn="978754282382xxx",
                        author_intro="",
                        book_intro="",
                        content="")
        assert code != 200

    def test_enew(self):
        drop_all_table()
        create_table()
        copy_data_to_book(DBSession())