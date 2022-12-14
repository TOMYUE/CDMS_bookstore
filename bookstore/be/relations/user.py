# -*- coding = utf-8 -*-
# @Time : 2022/11/23 19:54
# @File : user.py

from relations.init import *
from typing import *
import jwt
import time
import sqlalchemy
from add_books_for_search import *

def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.decode("utf-8")


def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded


def seller_login(uname: str, pwd: str, terminal: str):
    try:
        with db_session() as session:
            token = ""
            user = session.query(Seller).filter(Seller.uname == uname).first()
            if user is None :
                code, message = 502, "non_exist_user_id"
                return code, message, token
            if pwd != user.pwd:
                code, message = 501, "authorization failed"
                return code, message, token
            token = "token"
            user = session.query(Seller).filter(Seller.uname == uname).update({"token" : token})
            session.commit()
            return 200, "ok", token
    except Exception as e:
        return 500, f"Failure: {e}", token


def buyer_login(uname: str, pwd: str, terminal: str):
    try:
        with db_session() as session:
            token = ""
            user = session.query(Buyer).filter(Buyer.uname == uname).first()
            # user = self.session.execute("SELECT pwd FROM Buyer WHERE uid=:uid",{"uid":uid}).fetchone()
            if user is None :
                code, message = 502, "non_exist_user_id"
                return code, message, token
            if pwd != user.pwd:
                code, message = 501, "authorization failed"
                return code, message, token
            token = "token"
            user = session.query(Buyer).filter(Buyer.uname == uname).update({"token" : token})
            session.commit()
            return 200, "ok", token
    except Exception as e:
        return 500, f"Failure: {e}", token


def seller_logout(uname: str, token: str):
    try:
        with db_session() as session:
            user = session.query(Seller).filter(Seller.uname == uname).first()
            # user = self.session.execute("SELECT token from Seller WHERE uid='%s'"%(uid)).fetchone()
            # if user is None:  #?????????????????????
            #     return 502, f"non_exist_user_id{uname}"
            if user.token != token:
                return 501, "authorization failed"
            newtoken = token
            # session.execute("UPDATE Seller SET token='%s' WHERE uid='%s'" %(newtoken, uid))
            user = session.query(Seller).filter(Seller.uname == uname).update({"token": newtoken})
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"


def buyer_logout(uname: str, token: str):
    try:
        with db_session() as session:
            user = session.query(Buyer).filter(Buyer.uname == uname).first()
            # user = self.session.execute("SELECT token from Seller WHERE uid='%s'"%(uid)).fetchone()
            # if user is None: #???????????????
            #     return 501, "authorization failed"
            if user.token != token:
                return 501, "authorization failed"
            newtoken = "token"
            user = session.query(Buyer).filter(Buyer.uname == uname).update({"token": newtoken})
            # session.execute("UPDATE Seller SET token='%s' WHERE uid='%s'" % (newtoken, uid))
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"


def seller_register(uname: str, pwd: str, account: str, balance: float, token: str, terminal: str):
    try:
        with db_session() as session:
            user = session.query(Seller).filter(Seller.uname == uname).first()
            if user is None:
                seller = Seller(uname=uname,
                                   pwd=pwd,
                                   account=account,
                                   balance=balance,
                                   token=token,
                                   terminal=terminal)
                session.add(seller)
                session.flush()
                uid = seller.uid
                session.commit()
                return 200, "ok", uid
            else:
                return 502, "non_exist_user_id",-1
    except Exception as e:
        return 500, f"Failure: {e}"#, None


def buyer_register(uname: str, pwd: str, account: str, balance: float, token: str, terminal: str):
    terminal = "terminal_{}".format(str(time.time()))
    try:
        with db_session() as session:
            user = session.query(Buyer).filter(Buyer.uname == uname).first()
            if user is None:
                buyer = Buyer(uname=uname,
                      pwd=pwd,
                      account=account,
                      balance=balance,
                      token=token,
                      terminal=terminal)
                session.add(buyer)
                session.commit()
                session.flush()
                uid = buyer.uid
                return 200, "ok", uid
            else:
                return 502, "non_exist_user_id", -1
    except Exception as e:
        return 500, f"Failure: {e}"


def seller_unregister(uname: str, pwd: str):
    try:
        with db_session() as session:
            # user = session.execute("SELECT pwd FROM  Seller WHERE uid=:uid",{"uid": uid}).fetchone()
            user = session.query(Seller).filter(Seller.uname == uname).first()
            if user is None:
                code, message = 502, f"non_exist_user_id{uname}"
                return code, message
            if pwd != user.pwd:
                code, message = 501, "authorization failed"
                return code, message
            # session.execute("DELETE from Seller WHERE uid='%s'" %(uid))
            user = session.query(Seller).filter(Seller.uname == uname).delete()
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"


def buyer_unregister(uname: str, pwd: str):
    try:
        with db_session() as session:
            user = session.query(Buyer).filter(Buyer.uname == uname).first()
            if user is None:
                code, message = 502, f"non_exist_user_id{uname}"
                return code, message
            if pwd != user.pwd:
                code, message = 501, "authorization failed"
                return code, message
            # session.execute("DELETE from Seller WHERE uid='%s'" %(uid))
            user = session.query(Buyer).filter(Buyer.uname == uname).delete()
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"


def seller_change_password(uname: str, old_password: str, new_password: str):
    try:
        with db_session() as session:
            user = session.query(Seller).filter(Seller.uname == uname).first()
            if user is None:
                code, message = 502, f"non_exist_user_id{uname}"
                return code, message
            if old_password != user.pwd:
                code, message = 501, "authorization failed"
                return code, message
            # self.session.execute("UPDATE Seller SET pwd='%s' WHERE uid='%s'" %(new_password, uid))
            res = session.query(Seller).filter(Seller.uname == uname).update({"pwd":new_password})
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"


def buyer_change_password(uname: str, old_password: str, new_password: str):
    try:
        with db_session() as session:
            user = session.query(Buyer).filter(Buyer.uname == uname).first()
            if user is None:
                code, message = 502, f"non_exist_user_id{uname}"
                return code, message
            if old_password != user.pwd:
                code, message = 501, "authorization failed"
                return code, message
            res = session.query(Buyer).filter(Buyer.uname == uname).update({"pwd":new_password})
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"


#????????????????????????page???????????????????????????????????????
#???????????????????????????page??????1????????????
#???????????????page???0???????????????
def search_title(title:str, page:int):
    try:
        with db_session() as session:
            pageSize = 10
            if page > 0:
                results = session.query(Search_title, Book).filter(Search_title.title == title).filter(Book.bid == Search_title.book_id).order_by(Book.price).limit(pageSize).offset(pageSize * (page-1)).all()
            else:
                results = session.query(Search_title, Book).filter(Search_title.title == title).filter(Book.bid == Search_title.book_id).order_by(Book.price).all()
            if len(results) > 0:
                return 200, "ok"
            else:
                return 503, f"non_exist_book_id{title}"
    except Exception as e:
        return 500, f"Failure: {e}"


def search_title_in_store(title:str, page:int, sid:int):
    try:
        with db_session() as session:
            pageSize = 10
            stores = session.query(Store.sid).filter(Store.sid == sid).first()
            if stores is None:
                return 506, f"store_not_exists{sid}"
            if page > 0:
                results = session.query(Search_title,Book, Store).filter(Search_title.title == title).join(Store,Store.bid == Book.bid).\
                        filter(Store.sid == sid).order_by(Book.price).limit(pageSize).offset(pageSize * (page-1)).all()
            else:
                results = session.query(Book, Store).join(Store, Store.bid == Book.bid). \
                    filter(Book.title == title and Store.sid == sid).order_by(Book.price).all()
            if len(results):
                session.commit()
                return 200, "ok"
            else:
                session.commit()
                return 503, f"non_exist_book_id{title}"
    except Exception as e:
        return 500, f"Failure: {e}"

def search_tag(tag:str, page:int):
    try:
        with db_session() as session:
            pageSize = 10
            # results = session.query(Book).filter(Book.tags.contains(tag)).order_by(Book.price).limit(pageSize).offset(
            #     pageSize * max(0, page - 1)).all()

            if page > 0:
                results = session.query(Book,Search_tags).filter(Search_tags.tags == tag).filter(Book.bid == Search_tags.book_id).order_by(Book.price).limit(pageSize).offset(pageSize * (page-1)).all()
            else:
                results = session.query(Book,Search_tags).filter(Search_tags.tags == tag).filter(Book.bid == Search_tags.book_id).order_by(Book.price).all()
            if len(results):
                session.commit()
                return 200,"ok"
            else:
                session.commit()
                return 504, f"non_exist_tag{tag}"
    except Exception as e:
        return 500, f"Failure: {e}"


def search_tag_in_store(tag:str, page:int, sid:int):
    try:
        with db_session() as session:
            pageSize = 10
            stores = session.query(Store).filter(Store.sid == sid).first()
            if stores is None:
                return 506, f"store_not_exists{sid}"
            if page > 0:
                results = session.query(Book,Store,Search_tags).filter(Search_tags.tags == tag).join(Store, Store.bid == Book.bid).filter(Store.sid == sid).order_by(Book.price).limit(pageSize).offset(pageSize * (page-1)).all()
            else:
                results = session.query(Book,Store,Search_tags).filter(Search_tags.tags == tag).join(Store, Store.bid == Book.bid).filter(Store.sid == sid).order_by(Book.price).all()
            if len(results):
                session.commit()
                return 200,"ok"
            else:
                session.commit()
                return 504, f"non_exist_tag{tag}"
    except Exception as e:
        return 500, f"Failure: {e}"

def search_content(book_intro:str, page:int):
    try:
        with db_session() as session:
            pageSize = 10
            # results = session.query(Book).filter(Book.book_intro.contains(book_intro)).limit(pageSize).offset(pageSize * (page - 1)).all()
            # return 200, "ok"
            if page > 0:
                results = session.query(Book,Search_book_intro).filter(Search_book_intro.book_intro == book_intro).filter(Search_book_intro.book_id == Book.bid).limit(pageSize).offset(pageSize * (page - 1)).all()
            else:
                results = session.query(Book,Search_book_intro).filter(Search_book_intro.book_intro == book_intro).filter(Search_book_intro.book_id == Book.bid).all()
            if len(results):
                session.commit()
                return 200, "ok"
            else:
                session.commit()
                return 505, f"non_exist_such_content{book_intro}"
    except Exception as e:
        return 500, f"Failure:{e}"

def search_content_in_store(book_intro:str, page:int, sid:int):
    try:
        with db_session() as session:
            pageSize = 10
            stores = session.query(Store.sid).filter(Store.sid == sid).first()
            if stores is None:
                return 506, f"store_not_exists{sid}"
            if page > 0:
                results = session.query(Book,Store).filter(Search_book_intro.book_id == Book.bid).join(Store, Store.bid == Book.bid).filter(Book.book_intro.contains(book_intro)).filter(Store.sid == sid).limit(pageSize).offset(pageSize * (page - 1)).all()
            else:
                results = session.query(Book,Store).filter(Search_book_intro.book_id == Book.bid).join(Store, Store.bid == Book.bid).filter(Book.book_intro.contains(book_intro)).filter(Store.sid == sid).all()
            if len(results):
                session.commit()
                return 200, "ok"
            else:
                session.commit()
                return 505, f"non_exist_such_content{book_intro}"
    except Exception as e:
        return 500, f"Failure:{e}"

def search_author(author:str, page):
    try:
        with db_session() as session:
            pageSize = 10
            if page > 0:
                results = session.query(Book, Search_author).filter(Search_author.author == author).filter(Book.author == author).order_by(Book.price).limit(pageSize).offset(pageSize * (page-1)).all()
            else:
                results = session.query(Book).filter(Search_author.author == author).filter(Book.author == author).order_by(Book.price).all()
            if len(results):
                session.commit()
                return 200, "ok"
            else:
                session.commit()
                return 507, f"non_exist_book_author{author}"
    except Exception as e:
        return 500, f"Failure: {e}"


def search_author_in_store(author:str, page:int, sid:int):
    try:
        with db_session() as session:
            pageSize = 10
            stores = session.query(Store.sid).filter(Store.sid == sid).first()
            if stores is None:
                return 506, f"store_not_exists{sid}"
            if page > 0:
                results = session.query(Book, Store).filter(Search_author.author == author).join(Store,Store.bid == Book.bid).\
                        filter(Book.author == author and Store.sid == sid).order_by(Book.price).limit(pageSize).offset(pageSize * (page-1)).all()
            else:
                results = session.query(Book, Store).filter(Search_author.author == author).join(Store, Store.bid == Book.bid). \
                    filter(Book.author == author and Store.sid == sid).order_by(Book.price).all()
            if len(results):
                return 200, "ok"
            else:
                return 507, f"non_exist_book_id{author}"
    except Exception as e:
        return 500, f"Failure: {e}"