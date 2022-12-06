# -*- coding = utf-8 -*-
# @Time : 2022/11/23 19:54
# @File : user.py

from relations.init import *
from typing import *
import jwt
import time
import sqlalchemy

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
            # user = self.session.execute("SELECT pwd FROM Seller WHERE uid=:uid",{"uid":uid}).fetchone()
            if user is None :
                code, message = 502, "non_exist_user_id"
                return code, message, token
            if pwd != user.pwd:
                code, message = 501, "authorization failed"
                return code, message, token
            # token = jwt_encode("token", terminal)
            token = "token"
            user = session.query(Seller).filter(Seller.uname == uname).update({"token" : token})
            session.commit()
            # self.session.execute("UPDATE Seller set token= '%s' , terminal = '%s' where uid = '%s'" % (token, terminal, uid))
            # self.session.commit()
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
            # self.session.execute("UPDATE Buyer set token= '%s' , terminal = '%s' where uid = '%s'" % (token, terminal, uid))
            session.commit()
            return 200, "ok", token
    except Exception as e:
        return 500, f"Failure: {e}", token


def seller_logout(uname: str, token: str):
    try:
        with db_session() as session:
            user = session.query(Seller).filter(Seller.uname == uname).first()
            # user = self.session.execute("SELECT token from Seller WHERE uid='%s'"%(uid)).fetchone()
            # if user is None:  #这种情况不存在
            #     return 502, f"non_exist_user_id{uname}"
            if user.token != token:
                return 501, "authorization failed"
            newtoken = "token"
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
            # if user is None: #情况不存在
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
                session.add(Seller(uid=int(time.time()),
                                    uname=uname,
                                   pwd=pwd,
                                   account=account,
                                   balance=balance,
                                   token=token,
                                   terminal=terminal))
                session.commit()
                return 200, "ok"#, seller.uid
            else:
                return 502, "non_exist_user_id"
    except Exception as e:
        return 500, f"Failure: {e}"#, None


def buyer_register(uname: str, pwd: str, account: str, balance: float, token: str, terminal: str):
    terminal = "terminal_{}".format(str(time.time()))
    try:
        with db_session() as session:
            user = session.query(Buyer).filter(Buyer.uname == uname).first()
            if user is None:
                session.add(Buyer(uname=uname,
                                  pwd=pwd,
                                  account=account,
                                  balance=balance,
                                  token=token,
                                  terminal=terminal))
                session.commit()
                return 200, "ok"
            else:
                return 502, "non_exist_user_id"
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
