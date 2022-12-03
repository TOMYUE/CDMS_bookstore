from be.relations.init import *
from be.relations.buyer import *
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
def add_book(uid, sid, stock_level, *, 
    tags: List[str] = list(), 
    pictures: List[bytes] = list(),
    id: int,
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
            session.add(Store(
                sid = sid,
                uid = uid,
                bid = id,
                inventory_quantity = stock_level,
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
                pictures=",".join(pictures)
            ))
            session.commit()
        return 200, f"Success: add a book"
    except Exception as e:
        return 500, f"Failure: {e}"


def add_stock_level(uid, sid, bid, stock_level_delta):
    try: 
        with db_session() as session:
            result = session.query(Store)\
                .filter(Store.sid==sid and Store.bid==bid and Store.uid==uid)\
                .update({"inventory_quantity" : Store.inventory_quantity + stock_level_delta})
            if result == 0:
                if session.query(Store).filter(Store.sid==sid).count() == 0:
                    session.commit()
                    return 501, f"Failure: no such store"
                else:
                    return 502, f"Failure: no such book"
            session.commit()
        return 200, f"Success: {result}"
    except Exception as e:
        return 500, f"Failure: {e}"


def shipping(uid, sid, bid):
    try:
        with db_session() as session:
            filter_condition = (Deal.uid == uid) and (Deal.sid == sid) and (Deal.bid == bid) \
                               and (Deal.status == deal_status["付款"])
            buyer_deals = session.query(Deal).filter(filter_condition).all()
            for deal in buyer_deals:
                deal.status = deal_status["发货"]
                session.add(deal)
                session.commit()
    except Exception as e:
        return 500, f"Failure: {e}"