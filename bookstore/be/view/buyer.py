from fastapi import FastAPI
from relations import buyer
from typing import *
from typing_extensions import *
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class NewOrderForm(BaseModel):
    user_id: int
    store_id: int
    id_and_num: List[Tuple[str, int]]  # (id, num)


@app.post("/new_order")
async def new_order(form: NewOrderForm):
    code, msg, order_id = buyer.new_order(
        user_id=form.user_id,
        store_id=form.store_id,
        id_and_num=form.id_and_num
    )
    return JSONResponse({"message": msg, "order_id": order_id}, status_code=code)


class PaymentForm(BaseModel):
    user_id: int
    store_id: int


@app.post("/payment")
async def payment(form: PaymentForm):
    # 用户支付书籍订单的货款，如果账户余额不足，则取消订单
    code, msg = buyer.payment(
       user_id=form.user_id,
       store_id=form.store_id
    )
    return JSONResponse({"message": msg}, status_code=code)


class FundsForm(BaseModel):
    user_id: int
    add_value: int


@app.post("/add_funds")
async def add_funds(form: FundsForm):
    # 增加个人账户余额
    code, msg = buyer.add_funds(
       user_id=form.user_id,
       add_value=form.add_value
    )
    return JSONResponse({"message": msg}, status_code=code)


class ReceiveBookForm(BaseModel):
    user_id: int
    store_id: int
    deal_id: int


@app.post("/receive_book")
async def receive_book(form: ReceiveBookForm):
    code, msg = buyer.receive_book(
        user_id=form.user_id,
        sid=form.store_id,
        did=form.deal_id
    )
    return JSONResponse({"message": msg}, status_code=code)


class HistoryForm(BaseModel):
    user_id: int


@app.get("/history")
async def history(form: HistoryForm):
    code, msg = buyer.history(form.user_id)
    return JSONResponse({"message": msg}, status_code=code)


class Cancel_deal_form(BaseModel):
    user_id: int
    deal_id: int


@app.post("/cancel_deal")
async def cancel_deal(form: Cancel_deal_form):
    code, msg = buyer.cancel_deal(form.user_id, form.deal_id)
    return JSONResponse({"message": msg}, status_code=code)
