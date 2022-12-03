# -*- coding = utf-8 -*-
# @Time : 2022/11/23 19:54
# @File : user.py

from be.relations.init import *
from typing import *
from be.model import error
import  jwt
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


def seller_login(uid:int, pwd:str, terminal:str):
    try:
        with db_session() as session:
            token = ""
            user = session.query(Seller).filter(Seller.uid == uid).first()
            # user = self.session.execute("SELECT pwd FROM Seller WHERE uid=:uid",{"uid":uid}).fetchone()
            if user is None or pwd != user.pwd:
                code, message = error.error_authorization_fail()
                return code, message, token
            token = jwt_encode(uid, terminal)
            user = session.query(Seller).filter(Seller.uid == uid).update(token)
            session.commit()
            # self.session.execute("UPDATE Seller set token= '%s' , terminal = '%s' where uid = '%s'" % (token, terminal, uid))
            # self.session.commit()
            return 200, "ok", token
    except Exception as e:
        return 500, f"Failure: {e}", token

def buyer_login(uid:int, pwd:str, terminal:str):
    try:
        with db_session() as session:
            token = ""
            user = session.query(Buyer).filter(Buyer.uid == uid).first()
            # user = self.session.execute("SELECT pwd FROM Buyer WHERE uid=:uid",{"uid":uid}).fetchone()
            if user is None or pwd != user.pwd:
                code, message = error.error_authorization_fail()
                return code, message, token
            token = jwt_encode(uid, terminal)
            user = session.query(Buyer).filter(Buyer.uid == uid).update(token)
            # self.session.execute("UPDATE Buyer set token= '%s' , terminal = '%s' where uid = '%s'" % (token, terminal, uid))
            session.commit()
            return 200, "ok", token
    except Exception as e:
        return 500, f"Failure: {e}", token

def seller_logout(uid:int, token:str):
    try:
        with db_session() as session:
            user = session.query(Seller).filter(Seller.uid == uid).first()
            # user = self.session.execute("SELECT token from Seller WHERE uid='%s'"%(uid)).fetchone()
            if user is None:
                return error.error_authorization_fail()
            if user.token != token:
                return error.error_authorization_fail()
            newtoken = ""
            # session.execute("UPDATE Seller SET token='%s' WHERE uid='%s'" %(newtoken, uid))
            user = session.query(Seller).filter(Seller.uid == uid).update(newtoken)
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"

def buyer_logout(uid: int, token: str):
    try:
        with db_session() as session:
            user = session.query(Buyer).filter(Buyer.uid == uid).first()
            # user = self.session.execute("SELECT token from Seller WHERE uid='%s'"%(uid)).fetchone()
            if user is None:
                return error.error_authorization_fail()
            if user.token != token:
                return error.error_authorization_fail()
            newtoken = ""
            user = session.query(Buyer).filter(Buyer.uid == uid).update(newtoken)
            # session.execute("UPDATE Seller SET token='%s' WHERE uid='%s'" % (newtoken, uid))
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"

def seller_register(uid:int, uname:str, pwd:str):
    terminal = "terminal_{}".format(str(time.time()))
    try:
        with db_session() as session:
            token = ""
            # session.execute("INSERT INTO Seller(uid, uname, pwd, account,balance, token, terminal) values(:uid, :pwd, :account, 0, :token, :terminal",{"uid":uid, "uname":uname, "pwd":pwd,"account":"account_name","token":token,"terminal":terminal})
            session.add(Seller(uid = uid,
                               uname = uname,
                               pwd = pwd,
                               account = "account",
                               balance = 0,
                               token = token,
                               terminal = terminal))
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"

def buyer_register(uid:int, uname:str, pwd:str):
    terminal = "terminal_{}".format(str(time.time()))
    try:
        with db_session() as session:
            token = ""
            session.add(Buyer(uid=uid,
                               uname=uname,
                               pwd=pwd,
                               account="account",
                               balance=0,
                               token=token,
                               terminal=terminal))
            # session.execute("INSERT INTO Buyer(uid, uname, pwd, account,balance, token, terminal) values(:uid, :pwd, :account, 0, :token, :terminal",{"uid":uid, "uname":uname, "pwd":pwd,"account":"account_name","token":token,"terminal":terminal})
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"

def seller_unregister(uid:int, pwd:str):
    try:
        with db_session() as session:
            # user = session.execute("SELECT pwd FROM  Seller WHERE uid=:uid",{"uid": uid}).fetchone()
            user = session.query(Seller).filter(Seller.uid == uid).first()
            if user is None:
                code, message = error.error_authorization_fail()
                return code, message
            if pwd != user.pwd:
                code, message = error.error_authorization_fail()
                return code, message
            # session.execute("DELETE from Seller WHERE uid='%s'" %(uid))
            user = session.query(Seller).filter(Seller.uid == uid).delete()
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"

def buyer_unregister(uid:int, pwd:str):
    try:
        with db_session() as session:
            user = session.query(Buyer).filter(Buyer.uid == uid).first()
            if user is None:
                code, message = error.error_authorization_fail()
                return code, message
            if pwd != user.pwd:
                code, message = error.error_authorization_fail()
                return code, message
            # session.execute("DELETE from Seller WHERE uid='%s'" %(uid))
            user = session.query(Buyer).filter(Buyer.uid == uid).delete()
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"

def seller_change_password(uid:int, old_password:str, new_password:str):
    try:
        with db_session() as session:
            user = session.query(Seller).filter(Seller.uid == uid).first()
            if user is None or old_password != user.pwd:
                code, message = error.error_authorization_fail()
                return code, message
            # self.session.execute("UPDATE Seller SET pwd='%s' WHERE uid='%s'" %(new_password, uid))
            res = session.query(Seller).filter(Seller.uid == uid).update(Seller.pwd)
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"

def buyer_change_password(uid:int, old_password:str, new_password:str):
    try:
        with db_session() as session:
            user = session.query(Buyer).filter(Buyer.uid == uid).first()
            if user is None or old_password != user.pwd:
                code, message = error.error_authorization_fail()
                return code, message
            res = session.query(Buyer).filter(Buyer.uid == uid).update(Buyer.pwd)
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"