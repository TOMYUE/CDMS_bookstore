from fastapi import FastAPI
from view import auth
from view import seller
from view import buyer
from relations.init import init

def app(restore_tables=True):
    if restore_tables:
        init()
    app = FastAPI()
    app.mount("/auth", auth.app),
    app.mount("/buyer", buyer.app),
    app.mount("/seller", seller.app)
    return app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app(), host="127.0.0.1", port=8000)
