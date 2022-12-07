import time

from relations.init import *
from typing import *


# status of the deal, using 0, 1, 2, 3 to denote each stage
# 下单->付款->发货->收货
deal_status = {
    "下单": 0,
    "付款": 1,
    "发货": 2,
    "收货": 3,
    "取消": 4,
}

def new_order(user_id: int, store_id: int, id_and_num: List[Tuple[str, int]]) -> Tuple[int, str, List]:
    try:
        with db_session() as session:
            # check if user exists
            buyer = session.query(Buyer).filter(Buyer.uid == user_id).first()
            if buyer is None:
                return 501, f"error_non_exist_user_id{user_id}", []
            # check if store exists
            store = session.query(StoreOwner).filger(StoreOwner.sid == store_id).first()
            if store is None:
                return 502, f"error_non_exist_store_id{store_id}", []
            # add each into the deal
            for bid, b_num in id_and_num:
                if b_num <= 0:
                    continue
                store_book = session.query(Store).filter((Store.sid == store_id) and (Store.bid == bid)).first()
                if store_book is None:
                    return 503, f"book not in store {store_id}", []
                elif store_book.inventory_quantity < b_num:
                    # TODO: there is a problem if in all books that he buy, there's only one that have no enough num,
                    #  simply return is very much unnecessary
                    return 503, f"book not in store {bid}", []
                # update inventory_quantity
                store_book.inventory_quantity -= b_num
                session.add(store_book)
                # add new deal to the deal relation
                deal = Deal(uid=user_id, sid=store_id, bid=bid,
                            order_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                            status=deal_status["下单"], money=store_book.price * b_num)
                session.add(deal)

            # get all the deal that this customer buy recently
            # TODO: how to get the auto increment id of the deal, when it has just created
            filter_condition = (Deal.uid == user_id) and (Deal.sid == store_id) and (Deal.status == deal_status["下单"])
            buyer_deals = session.query(Deal).filter(filter_condition).all()
            # get all the deal id of this customers current deal
            deal_id = [i.did for i in buyer_deals]
            session.commit()
            return 200, "ok", deal_id
    except Exception as e:
        return 500, f"Failure: {e}", []


def payment(user_id: int, store_id: int) -> Tuple[int, str]:
    # 从deal的表中找出所有这个客户刚刚下单的所有图书的信息，并进行传入值检查，如果发现传入值有误，则进行一些列报错
    # SELECT * FROM deal WHERE uid=user_id and sid=store_id and status=deal_status["下单"]
    # 计算这笔交易的总金额为多少
    # 获取用户的账户金额信息，select balance from Buyer where uid=user_id
    # 如果账户金额小于图书总金额，报错，调用error函数
    # 如果账户金额足够支付，则
    # ——1. 扣款,更新账户信息 update Buyer set balance = new_balance
    # ——2. 商家的账户进账 update Seller set balance = new_balance
    # ——3. 所有图书的交易记录的状态进行更改 update Deal set status=deal_status["付款"]
    # ——4. 结束commit
    try:
        with db_session() as session:
            filter_condition = (Deal.uid == user_id) and (Deal.sid == store_id) and (Deal.status == deal_status["下单"])
            buyer_deals = session.query(Deal).filter(filter_condition).all()
            if buyer_deals is None:
                return 502, f"error_user_no_deal_exist {user_id}"
            total_price = 0
            for deal in buyer_deals:
                total_price += deal.money
            # get user balance
            buyer = session.query(Buyer).filter(Buyer.uid == user_id).first()
            if buyer is None:
                return 501, f"error_non_exist_user_id{user_id}"
            if buyer.balance < total_price:
                return 503, f"error_money_not_enough{user_id}"
            # buyer's balance is enough to buy all the book, uddate buyer balance
            buyer.balance -= total_price
            session.add(buyer)
            # get seller
            seller_id = session.query(StoreOwner.uid).filter(StoreOwner.sid == store_id).first().uid
            if seller_id is None:
                return 502, f"error_non_existent_store_id{store_id}"
            seller = session.query(Seller).filter(Seller.uid == seller_id).first()
            if seller is None:
                return 504, f"error_non_existent_user_id{seller_id}"
            seller.balance += total_price
            session.add(seller)

            # update each book deal
            for deal in buyer_deals:
                deal.status = deal_status["付款"]
                session.add(deal)

            session.commit()

        return 200, "ok"
    except Exception as e:
        return 500, f"Failure: {e}"


def add_funds(user_id, add_value) -> Tuple[int, str]:
    # 如果用户不存在直接报错
    # Invalid value check
    if add_value <= 0 or add_value > float('inf'):
        return 502, f"value cannot be added"
    try:
        with db_session() as session:
            buyer = session.query(Buyer).filter(Buyer.uid == user_id).first()
            # check user exists
            if buyer is None:
                return 501, f"error_non_exist_user_id{user_id}"
            # check is pwd matches
            # if buyer.pwd != password:
            #     return 504, f"authorization_fail"
            # user id exists and pwd matches, then update the balance for the user
            buyer.balance += add_value
            session.add(buyer)
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 530, "{}".format(str(e))


def receive_book(user_id, sid, did):
    try:
        with db_session() as session:
            filter_condition = (Deal.uid == user_id) and (Deal.sid == sid) and (Deal.did == did) \
                               and (Deal.status == deal_status["发货"])
            buyer_deals = session.query(Deal).filter(filter_condition).all()
            for deal in buyer_deals:
                deal.status = deal_status["收货"]
                session.add(deal)
                session.commit()
    except Exception as e:
        return 500,"{}".format(str(e))

# input: user id 
def query_deal_hist(uid):
    try: 
        with db_session() as session:
            deal_list = session.query(Deal).filter(Deal.uid == uid).all()
            session.commit()
        return 200, deal_list
    except Exception as e:
        return 500, f'{e}'

# input: user id, deal id
def cancel_deal(uid, did):
    try: 
        with db_session() as session:
            result = session.query(Deal)\
                .filter(Deal.uid == uid and Deal.did == did)
            bid = result.one().bid
            result.update({"status": deal_status["取消"]})
            session.query(Store)\
                .filter(Store.bid == bid)\
                .update({"inventory_quantity": Store.inventory_quantity+1})
            session.commit()
        return 200, f'{result}'
    except Exception as e:
        return 500, f'{e}'
