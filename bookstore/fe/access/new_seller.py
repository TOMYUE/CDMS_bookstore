from fe import conf
from fe.access import seller, auth


def register_new_seller(user_id, store_id, password, uname, account, balance) -> seller.Seller:
    a = auth.Auth(conf.URL)
    code = a.register_seller(user_id, store_id, password, uname, account, balance)
    assert code == 200
    s = seller.Seller(conf.URL, user_id, password)
    return s
