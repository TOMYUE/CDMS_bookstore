import logging
import os
from fastapi import FastAPI
from be.view import auth
from be.view import seller
from be.view import buyer
from be.model.store import init_database

app = FastAPI()

app.mount("/auth", auth.app),
app.mount("/buyer", buyer.app),
app.mount("/seller", seller.app)

def be_run():
    this_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(this_path)
    log_file = os.path.join(parent_path, "app.log")
    init_database(parent_path)

    logging.basicConfig(filename=log_file, level=logging.ERROR)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    )
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    import uvicorn
    uvicorn.run(app, port=5000, host='127.0.0.1')
