import time

from be.relations.init import *
from typing import *
from sqlalchemy import and_,or_
from sqlalchemy import func, extract


# status of the deal, using 0, 1, 2, 3 to denote each stage
# 下单->付款->发货->收货
deal_status = {
    "下单": 0,
    "付款": 1,
    "发货": 2,
    "收货": 3
}


def new_order(self, user_id: int, store_id: int, id_and_num: List[Tuple[int, int]]) -> Tuple[int, str, List]:
    try:
        with db_session() as session:
            # check if user exists
            buyer = session.query(Buyer).filter(Buyer.uid == user_id).first()
            if buyer is None:
                return error_non_exist_user_id(user_id)
            # check if store exists
            store = session.query(StoreOwner).filger(StoreOwner.sid == store_id).first()
            if store is None:
                return error_non_exist_store_id(store_id)
            # add each into the deal
            for bid, b_num in id_and_num:
                if b_num <= 0:
                    continue
                store_book = session.query(Store).filter((Store.sid == store_id) and (Store.bid == bid)).first()
                if store_book is None:
                    return error_no_book_sell_in_store(store_id)
                elif store_book.inventory_quantity < b_num:
                    # TODO: there is a problem if in all books that he buy, there's only one that have no enough num,
                    #  simply return is very much unnecessary
                    return error_stock_level_low(bid)
                # update inventory_quantity
                store_book.inventory_quantity -= b_num
                session.add(store_book)
                # add new deal to the deal relation
                deal = Deal(uid=user_id, sid=store_id,
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


def payment(self, user_id: int, password: str, store_id: int) -> Tuple[int, str]:
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
                return error_user_no_deal_exist(user_id)
            total_price = 0
            for deal in buyer_deals:
                total_price += deal.money
            # get user balance
            buyer = session.query(Buyer).filter(Buyer.uid == user_id).first()
            if buyer is None:
                return error_non_exist_user_id(user_id)
            if buyer.balance < total_price:
                return error_not_sufficient_funds(store_id)
            # buyer's balance is enough to buy all the book, uddate buyer balance
            buyer.balance -= total_price
            session.add(buyer)
            # get seller
            seller_id = session.query(StoreOwner.uid).filter(StoreOwner.sid == store_id).first().uid
            if seller_id is None:
                return error_non_exist_store_id(store_id)
            seller = session.query(Seller).filter(Seller.uid == seller_id).first()
            if seller is None:
                return error_non_exist_user_id(seller_id)
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


def add_funds(self, user_id, password, add_value) -> Tuple[int, str]:
    # 如果用户不存在直接报错
    # Invalid value check
    if add_value <= 0 or add_value > float('inf'):
        return error_invalid_add_value(user_id)
    try:
        with db_session() as session:
            buyer = session.query(Buyer).filter(Buyer.uid == user_id).first()
            # check user exists
            if buyer is None:
                return error_non_exist_user_id(user_id)
            # check is pwd matches
            if buyer.pwd != password:
                return error_authorization_fail()
            # user id exists and pwd matches, then update the balance for the user
            buyer.balance += add_value
            session.add(buyer)
            session.commit()
            return 200, "ok"
    except Exception as e:
        return 530, "{}".format(str(e))

