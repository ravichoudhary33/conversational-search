from fastapi import FastAPI, UploadFile, Request
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
from agents import create_agent, tools, llm

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

agent_user_map = {}


@app.get("/")
def read_root():
    return {"Hello": "World"}


class TextRequest(BaseModel):
    text: str
    convo_id: str

class Product(BaseModel):
    productId: int
    productName: str
    imgUrl: str
    price: float

class TextResponse(BaseModel):
    text: str
    filter: list[str]
    Products: list[Product]
    convo_id: str

@app.post("/sites/{sitekey}/chatbot", response_model=TextResponse)
def get_text_chat_response(sitekey,request: TextRequest,query_request : Request):
    # Process the request and generate the response
    query_params = query_request.query_params
    userid = query_params.get('uid')


    if userid in convo_history:
        langchain_info = convo_history[userid]
    else:
        langchain_info = newLangChainModel()
        convo_id = "1234567891234567"
        convo_history[userid] = langchain_info

    text = "Sure, here are a few shirts for "+userid+" "+ request.convo_id + " "+ sitekey
    filter_options = ["hrx", "Raymond", "Below 5K"]
    if(request.text.lower() =="hello"):
        text = "Hello how are you"
        filter_options = ["Loui phillip", "Levis", "Above 5K",'Below 2k','red']
    if(request.text.lower() =="hi"):
        text = "Hola!!!"
        filter_options = ["Raymond", "Pepe", "Blue",'Above 1K']
    products = [
        Product(productId=123, productName="Loui Phillip Shirt", imgUrl="https://picsum.photos/200/300",price=2400),
        Product(productId=456, productName="One Shirt", imgUrl="https://picsum.photos/200/300",price=2500),
        Product(productId=456, productName="Two Shirt", imgUrl="https://picsum.photos/200/300",price=2800),
        Product(productId=456, productName="Two Shirt", imgUrl="https://picsum.photos/200/300",price=2800),
        Product(productId=456, productName="Two Shirt", imgUrl="https://picsum.photos/200/300",price=2800),
        Product(productId=456, productName="Two Shirt", imgUrl="https://picsum.photos/200/300",price=2800),
        # Add more product objects as needed
    ]

    response = TextResponse(text=text, filter=filter_options, Products=products,convo_id=request.convo_id)
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
        Product(productId=123, productName="Loui Phillip Shirt", imgUrl="https://picsum.photos/200/300"),
        Product(productId=456, productName="Another Shirt", imgUrl="https://picsum.photos/200/300"),
        # Add more product objects as needed
    ]

    response = TextResponse(text=text, filter=filter_options, Products=products)
    return response
