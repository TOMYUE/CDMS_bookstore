from fastapi import FastAPI
from be.model.buyer import Buyer
from typing import *
from typing_extensions import *
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    uid: int
    uname: str
    pwd: str
    account: str
    balance: int


class Order(BaseModel):
    user_id: int
    store_id: int
    books: List[Tuple[int, int]]


@app.post("/new_order")
def new_order(order: Order):
    buyer = Buyer()
    code, msg, order_id = buyer.new_order(
        user_id = order.user_id,
        store_id = order.store_id,
        id_and_count = order.books
    )
    return JSONResponse({"message": msg, "order_id": order_id}, status_code=code)


@app.post("/payment")
def payment(usr: User, order: Order):
    # 用户支付书籍订单的货款，如果账户余额不足，则取消订单
    buyer = Buyer()
    code, msg = buyer.payment(
       usr.uid,
       usr.pwd,
       order.store_id
    )
    return JSONResponse({"message": msg}, status_code=code)


@app.post("/add_funds")
def add_funds(add_value: int, usr: User):
    # 增加个人账户余额
    buyer = Buyer()
    code, msg = buyer.add_funds(
        usr.uid,
        usr.pwd,
        add_value
    )
    return JSONResponse({"message": msg}, status_code=code)
