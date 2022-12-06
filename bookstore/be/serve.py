import logging
import os
from fastapi import FastAPI
from view import auth
from view import seller
from view import buyer
# from model.store import init_database
import uvicorn
import asyncio

app = FastAPI()

app.mount("/auth", auth.app),
app.mount("/buyer", buyer.app),
app.mount("/seller", seller.app)

server = uvicorn.Server(uvicorn.Config(app, port=5000, host='127.0.0.1'))

def run(test: bool):
    global server
    # this_path = os.path.dirname(__file__)
    # parent_path = os.path.dirname(this_path)
    # log_file = os.path.join(parent_path, "app.log")
    # init_database(parent_path)
    # logging.basicConfig(filename=log_file, level=logging.ERROR)
    # handler = logging.StreamHandler()
    # formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    # handler.setFormatter(formatter)
    # logging.getLogger().addHandler(handler)
    server.startup()
