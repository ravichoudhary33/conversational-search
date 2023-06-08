from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


class ImageRequest(BaseModel):
    image: UploadFile



@app.post("/api/getImageResponse", response_model=TextResponse)
def get_image_chat_response(request: TextRequest):
    # Process the image and generate the response
    image = Image.open(BytesIO(request.image.file.read()))
    # Perform necessary image processing or analysis on 'image'

    text = "Sure, here are a few shirts"
    filter_options = ["hrx", "Raymond", "Below 5K"]
    products = [
        Product(productId=123, productName="Loui Phillip Shirt", imgUrl="https://s3......png"),
        Product(productId=456, productName="Another Shirt", imgUrl="https://s3......png"),
        # Add more product objects as needed
    ]

    response = TextResponse(text=text, filter=filter_options, Products=products)
    return response
