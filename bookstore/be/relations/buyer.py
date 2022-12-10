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
            store = session.query(StoreOwner).filter(StoreOwner.sid == store_id).first()
            if store is None:
                return 502, f"error_non_exist_store_id{store_id}", []
            # add each into the deal
            for bid, b_num in id_and_num:
                if b_num <= 0:
                    continue
                store_book = session.query(Store).filter((Store.sid == store_id) and (Store.bid == bid)).first()
                book_info = session.query(Book).filter((Book.bid == bid)).first()
                book_price = book_info.price
                if store_book is None:
                    return 503, f"book not in store {store_id}", []
                elif store_book.inventory_quantity < b_num:
                    return 503, f"book not in store {bid}", []
                # update inventory_quantity
                store_book.inventory_quantity -= b_num
                session.add(store_book)
                # add new deal to the deal relation
                deal = Deal(uid=user_id, sid=store_id, bid=bid,
                            order_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                            status=deal_status["下单"], money=store_book.price * b_num, amount=b_num)
                session.add(deal)
            res = session.execute(f'''select * from "Deal";''')
            deal_id = []
            for i in res:
                print(i[1])
                deal_id.append(i.did)
            session.commit()
            return 200, "ok", deal_id
    except Exception as e:
        return 500, f"Failure: {e}", []


def payment(user_id: int, store_id: int) -> Tuple[int, str]:
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
            print(user_id)
            buyer = session.query(Buyer).filter(Buyer.uid == user_id).first()
            if buyer is None:
                return 501, f"error_non_exist_user_id{user_id}"
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
            return 200, "success"
    except Exception as e:
        return 500,"{}".format(str(e))


# input: user id 
def history(uid):
    try: 
        with db_session() as session:
            deal_list = session.query(Deal).filter(Deal.uid == uid).all()
            session.commit()
        return 200, [deal.dict() for deal in deal_list]
    except Exception as e:
        return 500, f'{e}'


# input: user id, deal id
def cancel_deal(uid, did):
    try:
        with db_session() as session:
            result = session.query(Deal)\
                .filter(Deal.uid == uid and Deal.did == did)
            deal = result.one()
            bid = deal.bid
            amount = deal.amount
            money = deal.money
            sid = deal.sid
            uid = deal.uid
            store = session.query(Store)\
                .filter(Store.bid == bid)\
                .filter(Store.sid == sid)
            seller_id = store.one().uid
            store.update({"inventory_quantity": Store.inventory_quantity+amount})
            session.query(Buyer)\
                .filter(Buyer.uid == uid)\
                .update({Buyer.balance: Buyer.balance+money})
            session.query(Seller)\
                .filter(Seller.uid == seller_id)\
                .update({Seller.balance: Seller.balance+money})
            result.update({"status": deal_status["取消"]})
            session.commit()
        return 200, f'{result}'
    except Exception as e:
        return 500, f'{e}'
