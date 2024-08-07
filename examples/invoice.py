import uvicorn
from fastapi import FastAPI

from icryptopay import ICryptoPay
from icryptopay.enums.http import HTTPMethod
from icryptopay.types.update import Update

app: FastAPI = FastAPI()
crypto: ICryptoPay = ICryptoPay(
    token="TOKEN",
    use_test_network=True
)


@crypto.pay_handler()
async def invoice_paid(update: Update) -> None:
    print("PAID")
    print(update)


@app.on_event("startup")
async def create_invoice() -> None:
    invoice = await crypto.create_invoice(asset="TON", amount=0.1)
    print(invoice.bot_invoice_url)


@app.on_event("shutdown")
async def close_session() -> None:
    await crypto.close()


if __name__ == "__main__":
    app.add_route(path="/", route=crypto.get_updates, methods=[HTTPMethod.POST])
    uvicorn.run(app=app, host="localhost", port=3001)
