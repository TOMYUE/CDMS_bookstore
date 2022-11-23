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

class User:
    def __init__(self):
        db.__init__(self)

    def seller_login(self, uid:int, pwd:str, terminal:str):
        token = ""
        user = self.session.execute("SELECT pwd FROM Seller WHERE uid=:uid",{"uid":uid}).fetchone()
        if user is None or pwd != user.pwd:
            code, message = error.error_authorization_fail()
            return code, message, token
        token = jwt_encoder(uid, terminal)
        self.session.execute("UPDATE Seller set token= '%s' , terminal = '%s' where uid = '%s'" % (token, terminal, uid))
        self.session.commit()
        return 200, "ok", token

    def buyer_login(self, uid:int, pwd:str, terminal:str):
        token = ""
        user = self.session.execute("SELECT pwd FROM Buyer WHERE uid=:uid",{"uid":uid}).fetchone()
        if user is None or pwd != user.pwd:
            code, message = error.error_authorization_fail()
            return code, message, token
        token = jwt_encoder(uid, terminal)
        self.session.execute("UPDATE Buyer set token= '%s' , terminal = '%s' where uid = '%s'" % (token, terminal, uid))
        self.session.commit()
        return 200, "ok", token

    def seller_logout(self, uid:int, token:str):
        try:
            user = self.session.execute("SELECT token from Seller WHERE uid='%s'"%(uid)).fetchone()
            if user is None:
                return error.error_authorization_fail()
            if user.token != token:
                return error.error_authorization_fail()
            newtoken = ""
            self.session.execute("UPDATE Seller SET token='%s' WHERE uid='%s'" %(newtoken, uid))
            self.session.commit()
            return 200, "ok"
        except sqlalchemy.exc.IntegrityError:
            return error.error_authorization_fail()

    def buyer_logout(self, uid: int, token: str):
        try:
            user = self.session.execute("SELECT token from Buyer WHERE uid='%s'" % (uid)).fetchone()
            if user is None:
                return error.error_authorization_fail()
            if user.token != token:
                return error.error_authorization_fail()
            newtoken = ""
            self.session.execute("UPDATE Buyer SET token='%s' WHERE uid='%s'" % (newtoken, uid))
            self.session.commit()
            return 200, "ok"
        except sqlalchemy.exc.IntegrityError:
            return error.error_authorization_fail()

    def seller_register(self, uid:int, pwd:str):
        terminal = "terminal_{}".format(str(time.time()))
        try:
            token = ""
            self.session.execute("INSERT INTO Seller(uid, uname, pwd, account,balance, token, terminal) values(:uid, :pwd, :account, 0, :token, :terminal",{"uid":uid, "uname":uname, "pwd":pwd,"account":"account_name","token":token,"terminal":terminal})
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return error.error_non_exist_user_id()

    def buyer_register(self, uid:int, pwd:str):
        terminal = "terminal_{}".format(str(time.time()))
        try:
            token = ""
            self.session.execute("INSERT INTO Buyer(uid, uname, pwd, account,balance, token, terminal) values(:uid, :pwd, :account, 0, :token, :terminal",{"uid":uid, "uname":uname, "pwd":pwd,"account":"account_name","token":token,"terminal":terminal})
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return error.error_non_exist_user_id()

    def seller_unregister(self, uid:int, pwd:str):
        user = self.session.execute("SELECT pwd FROM  Seller WHERE uid=:uid",{"uid": uid}).fetchone()
        if user is None:
            code, message = error.error_authorization_fail()
            return code, message
        if pwd != user.pwd:
            code, message = error.error_authorization_fail()
            return code, message
        self.session.execute("DELETE from Seller WHERE uid='%s'" %(uid))
        self.session.commit()
        return 200, "ok"

    def buyer_unregister(self, uid:int, pwd:str):
        user = self.session.execute("SELECT pwd FROM Buyer WHERE uid=:uid",{"uid": uid}).fetchone()
        if user is None:
            code, message = error.error_authorization_fail()
            return code, message
        if pwd != user.pwd:
            code, message = error.error_authorization_fail()
            return code, message
        self.session.execute("DELETE from Buyer WHERE uid='%s'" %(uid))
        self.session.commit()
        return 200, "ok"

    def seller_change_password(self, uid:int, old_password:str, new_password:str):
        user = self.session.execute("SELECT pwd FROM Seller WHERE uid='%s'" %(uid)).fetchone()
        if user is None or old_password != user.pwd:
            code, message = error.error_authorization_fail()
            return code, message
        self.session.execute("UPDATE Seller SET pwd='%s' WHERE uid='%s'" %(new_password, uid))
        self.session.commit()
        return 200, "ok"

    def buyer_change_password(self, uid:int, old_password:str, new_password:str):
        user = self.session.execute("SELECT pwd FROM Buyer WHERE uid='%s'" %(uid)).fetchone()
        if user is None or old_password != user.pwd:
            code, message = error.error_authorization_fail()
            return code, message
        self.session.execute("UPDATE Seller SET pwd='%s' WHERE uid='%s'" %(new_password, uid))
        self.session.commit()
        return 200, "ok"