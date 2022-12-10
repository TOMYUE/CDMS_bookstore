from relations.init import *
from relations.buyer import *
from typing import *


# uid: user_id
# sid: store_id
def create_store(uid, sid):
    try: 
        with db_session() as session:
            session.add(StoreOwner(uid=uid, sid=sid))
            session.commit()
        return 200, "Success: a new store"
    except Exception as e:
        return 500, f"Failure: {e}"


# uid: user_id
# sid: store_id
def add_book(*, 
    tags: List[str] = list(), 
    pictures: List[bytes] = list(),
    id: str,
    title: str,
    author: str,
    publisher: str,
    original_title: str,
    translator: str,
    pub_year: str,
    pages: int,
    price: int,
    binding: str,
    isbn: str,
    author_intro: str,
    book_intro: str,
    content: str
):
    try:
        with db_session() as session:
            session.add(Book(
                bid = id,
                title = title,
                author = author,
                publisher = publisher,
                original_title = original_title,
                translator = translator,
                pub_year = pub_year,
                pages = pages,
                price = price,
                currency_unit = "元",
                binding = binding,
                isbn = isbn,
                author_intro = author_intro,
                book_intro = book_intro,
                content = content,
                tags = ",".join(tags),
                picture=",".join(pictures)
            ))
            session.commit()
        return 200, f"Success: add a book"
    except Exception as e:
        return 500, f"Failure: {e}"


def add_stock_level(uid, sid, bid, stock_level_delta):
    try: 
        with db_session() as session:
            ownership = session.query(StoreOwner)\
                .filter(StoreOwner.sid==sid and StoreOwner.uid==uid).count
            if ownership == 0:
                session.commit() 
                raise Exception("user doesn't own this store")
            result = session.query(Store)\
                .filter(Store.sid==sid)\
                .filter(Store.uid==uid)\
                .filter(Store.bid==bid)\
                .update({"inventory_quantity": Store.inventory_quantity+stock_level_delta})
            if result == 0:
                result = session.add(Store(sid=sid, bid=bid, uid=uid, inventory_quantity=stock_level_delta))
            session.commit()
        return 200, f"Success: {result}"
    except Exception as e:
        return 500, f"Failure: {e}"

def change_price(sid, bid, price):
    try: 
        with db_session() as session:
            result = session.query(Store)\
                .filter(Store.sid==sid)\
                .filter(Store.bid==bid)\
                .update({Store.price: price})
            if result == 0:
                raise Exception("no such book to update")
            session.commit()
        return 200, f"Success: update {result}"
    except Exception as e:
        return 500, f"Failure: {e}"

def query_stock_level(_, sid, bid):
    try: 
        with db_session() as session:
            result = session.query(Store.inventory_quantity)\
                .filter(Store.sid==sid)\
                .filter(Store.bid==bid)\
                .one_or_none()
            session.commit()
        return 200, result["inventory_quantity"]
    except Exception as e:
        return 500, f"Failure: {e}"

def shipping(uid, sid, bid):
    try:
        with db_session() as session:
            filter_condition = (
                Deal.uid == uid and 
                Deal.sid == sid and 
                Deal.bid == bid and 
                Deal.status == deal_status["付款"]
            )
            buyer_deals = session.query(Deal).filter(filter_condition).all()
            for deal in buyer_deals:
                deal.status = deal_status["发货"]
                session.add(deal)
            session.commit()
        return 200, "Success: ok"
    except Exception as e:
        return 500, f"Failure: {e}"
