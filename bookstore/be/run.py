from fastapi import FastAPI
from view import auth
from view import seller
from view import buyer

app = FastAPI()

app.mount("/auth", auth.app),
app.mount("/buyer", buyer.app),
app.mount("/seller", seller.app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
