# from fe import conf
# from fe.access import buyer, auth
#
#
# def register_new_buyer(user_id, password) -> buyer.Buyer:
#     a = auth.Auth(conf.URL)
#     code = a.register(user_id, password)
#     assert code == 200
#     s = buyer.Buyer(conf.URL, user_id, password)
#     return s

from fe import conf
from fe.access import auth
from be.relations.init import DBSession, Buyer


def register_new_buyer(uid: int, pwd: str, uname: str, account: str, balance: float):
    """Add new registered buyer info into the database"""
    a = auth.Auth(conf.URL)
    session = DBSession()
    receive_buyer_info_status_code = a.register_buyer(uid, pwd, uname, account, balance)
    assert receive_buyer_info_status_code == 200
    new_buyer = Buyer(
        uid=uid, uname=uname, pwd=pwd, account=account, balance=balance
    )
    with session.begin():
        try:
            session.add(new_buyer)
        except:
            return "500"
    return new_buyer

