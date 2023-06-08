from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class TextRequest(BaseModel):
    text: str
    user_id: str
    site_key: str

class Product(BaseModel):
    productId: int
    productName: str
    imgUrl: str
    price: float

class TextResponse(BaseModel):
    text: str
    filter: list[str]
    Products: list[Product]

@app.post("/api/getTextChatResponse", response_model=TextResponse)
def get_text_chat_response(request: TextRequest):
    # Process the request and generate the response
    text = "Sure, here are a few shirts"
    filter_options = ["hrx", "Raymond", "Below 5K"]
    products = [
        Product(productId=123, productName="Loui Phillip Shirt", imgUrl="https://s3......png",price=2400),
        Product(productId=456, productName="Another Shirt", imgUrl="https://s3......png",price=2500),
        # Add more product objects as needed
    ]

    response = TextResponse(text=text, filter=filter_options, Products=products)
    return response



