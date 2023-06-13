from fastapi import FastAPI, UploadFile, Request
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
# from agents import create_agent, tools, llm
from schemas import Product
from chat import chat
from query_filter_state_agent import QueryFilterStateAgent
import openai
import json
from vector_store import createVectorStore

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

convo_history = {}
vector_store = createVectorStore()
queryFilterStateAgent = QueryFilterStateAgent(vector_store)

@app.get("/")
def read_root():
    return {"Hello": "World"}


class TextRequest(BaseModel):
    text: str
    convo_id: str

class TextResponse(BaseModel):
    product_summary_resp: str
    assistant_resp: str
    as_resp: str
    suggested_queries: list[str] = []
    suggested_filters: list[str] = []
    products: list[Product] = []

@app.post("/sites/{sitekey}/chatbot", response_model=TextResponse)
def get_text_chat_response(sitekey,request: TextRequest,query_request : Request):
    # Process the request and generate the response
    query_params = query_request.query_params
    userid = query_params.get('uid')


    # if userid in convo_history:
    #     langchain_info = convo_history[userid]
    # else:
    #     langchain_info = create_agent(llm, tools)
    #     convo_id = "1234567891234567"
    #     convo_history[userid] = langchain_info

    # text, filter_options, products = chat(langchain_info, request.text)
    # print(text, filter_options, products)
    try:
        product_summary_resp, assistant_resp, as_resp, suggested_queries, suggested_filters, products = queryFilterStateAgent.collect_message(userid, request.text)
    except openai.error.RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")
        product_summary_resp, assistant_resp, as_resp, suggested_queries, suggested_filters, products = [""]*6
    print(product_summary_resp, assistant_resp, as_resp, suggested_queries, suggested_filters, products)

    # text = "Sure, here are a few shirts for "+userid+" "+ request.convo_id + " "+ sitekey
    # filter_options = ["hrx", "Raymond", "Below 5K"]
    # # if(request.text.lower() =="hello"):
    # #     text = "Hello how are you"
    # #     filter_options = ["Loui phillip", "Levis", "Above 5K",'Below 2k','red']
    # # if(request.text.lower() =="hi"):
    # #     text = "Hola!!!"
    # #     filter_options = ["Raymond", "Pepe", "Blue",'Above 1K']
    # products = [
    #     Product(productId=123, productName="Loui Phillip Shirt", imgUrl="https://picsum.photos/200/300",price=2400),
    #     Product(productId=456, productName="One Shirt", imgUrl="https://picsum.photos/200/300",price=2500),
    #     Product(productId=456, productName="Two Shirt", imgUrl="https://picsum.photos/200/300",price=2800),
    #     Product(productId=456, productName="Two Shirt", imgUrl="https://picsum.photos/200/300",price=2800),
    #     Product(productId=456, productName="Two Shirt", imgUrl="https://picsum.photos/200/300",price=2800),
    #     Product(productId=456, productName="Two Shirt", imgUrl="https://picsum.photos/200/300",price=2800),
    #     # Add more product objects as needed
    # ]
    #
    # response = TextResponse(text=text, filter=filter_options, Products=products,convo_id=request.convo_id)
    response = TextResponse(
        product_summary_resp=product_summary_resp,
        assistant_resp=assistant_resp,
        as_resp=as_resp,
        suggested_queries=suggested_queries,
        suggested_filters=suggested_filters,
        products=products
    )
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
