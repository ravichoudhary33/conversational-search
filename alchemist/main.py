from fastapi import FastAPI, Request, Response
import datetime
from pydantic import BaseModel, parse_obj_as
import json
from datadog import statsd
from uuid import UUID
import uuid
from typing import Dict,List,Optional
#from alchemist import REDIS_HOST,REDIS_ENTRIES
import redis
REDIS_ENTRIES = 3
from downstream import reranker_client, brewer_client, top_query_brewer_client

REDIS_HOST = 'redis'

app = FastAPI()


def collect_message(userId, text):
    return ("123123","Bye", [],[],[])


with open('affinity.json') as file:
    affinity = json.load(file)
    print(affinity)

r = redis.Redis(host=REDIS_HOST, port=6379, db=0)

try:
    r.ping()
    print("Redis is running locally.")
except redis.exceptions.ConnectionError:
    print("Redis is not running or not accessible.")

class BotRequest(BaseModel):
    convo_id: str
    text: str

class Product(BaseModel):
    title: str
    imageUrl: List[str]
    listPrice: str
    salePrice: str

class BotResponsePrompts(BaseModel):
    text: Optional[str]
    filter: Optional[List[str]]
    autosuggest: Optional[List[str]]
    products: Optional[List[Product]]

class BotResponse(BaseModel):
    convo_id: str
    response: BotResponsePrompts

@app.post("/sites/{sitekey}/chatbot")
@statsd.timed('requests', tags=["api:text", "method:post"])
async def facet_affinity(sitekey,request : Request, ):
    # products = [
    #     Product(productId=123, productName="Loui Phillip Shirt", imgUrl="https://picsum.photos/200/300",price=2400),
    #     Product(productId=456, productName="One Shirt", imgUrl="https://picsum.photos/200/300",price=2500),
    #     Product(productId=456, productName="Two Shirt", imgUrl="https://picsum.photos/200/300",price=2800),
    #     Product(productId=456, productName="Two Shirt", imgUrl="https://picsum.photos/200/300",price=2800),
    #     Product(productId=456, productName="Two Shirt", imgUrl="https://picsum.photos/200/300",price=2800),
    #     Product(productId=456, productName="Two Shirt", imgUrl="https://picsum.photos/200/300",price=2800),
    #     # Add more product objects as needed
    # ]

    # response = TextResponse(Products=products)
    
    start = datetime.datetime.now()
    query_params = request.query_params
    body = await request.json()
    botRequest = parse_obj_as(BotRequest, body) 
    print(botRequest.convo_id)

    userId = query_params.get('uid')
    print(userId)

    check_bot_Input = checkQueryParams(query_params, botRequest)
    print(check_bot_Input)
    botResponse = init_bot(botRequest, check_bot_Input, userId, sitekey)
    #response = Response(content=botResponse, media_type="application/json")
    return botResponse

def init_bot(botRequest, botInput, userId, sitekey):
    convo_id = botRequest.convo_id
    if convo_id is None or len(str(convo_id))<1:
        if botInput == "query":
            botResponsePrompts = initNewQueryConvo(userId, sitekey, botRequest)
        elif botInput == "TS":
            botResponsePrompts = initTopSeller(sitekey, userId)
        elif botInput == "RFU":
            botResponsePrompts = initRFU(sitekey, userId)
        # elif botInput == "image":
        #     initNewImageConvo()
    elif (convo_id is not None and len(str(convo_id))>1):
        botResponsePrompts = initRedis(convo_id,userId, sitekey)
    botResponse = BotResponse(convo_id=convo_id, response=botResponsePrompts)
    return botResponse

def checkQueryParams(query_params, botRequest):
    isImage = 'false'
    isFilter = 'false'
    isRFU = 'false'
    isTS = 'false'
    query = ""
    if botRequest.text is not None and len(botRequest.text)>1:
        query = botRequest.text
    if 'filter' in query_params:
        isFilter = query_params.get('filter')
    if 'RFU' in query_params:
        isRFU =  query_params.get('RFU')
    if 'TS' in query_params:
        isTS =  query_params.get('TS')
    if 'image' in query_params:
        isImage = query_params.get('image')
    
    if isImage == 'true':
        return "image"
    elif isRFU == 'true':
        return "RFU"
    elif isTS == 'true':
        return "TS"
    elif (len(query)>1):
        return "query"
    else: 
        return "filter"
    
def initNewQueryConvo(userId, sitekey , botRequest):

    #generate new uuid
    convo_id = str(uuid.uuid4().hex)[:16]
    botRequest.convo_id = convo_id

    #update redis
    if r.exists(f'{userId}'):
        redis_value = r.get(f'{userId}')
        r.set(f'{userId}',update_redis_entries(redis_value, convo_id, None))
    else:
        r.set(f'{userId}',add_convo_id({}, convo_id, None))
    
    #call open AI library 
    ## TBD

    #Call reranker
    facets, var_facets = reranker_client(sitekey, userId)

    #### Call chatgpt to get relevant results or langchain specific results
    #queryFilterStateAgent = QueryFilterStateAgent()
    model_response = list(collect_message(userId, botRequest.text))
    model_history = model_response[0] #product hist
    sugg_prompt = model_response[1] #prompt hist
    sugg_queries = model_response[2] #autosugg hist
    sugg_filters = model_response[3]
    sugg_pdts = model_response[4]

    botResponsePrompts = BotResponsePrompts(text=sugg_prompt, filter=sugg_filters, autosuggest=sugg_queries, products=sugg_pdts)
    
    redis_value = r.get(f'{userId}')
    json_str = redis_value.decode()
    val = json.loads(json_str)
    r.set(f'{userId}',add_convo_id(val, convo_id, model_history))

    return botResponsePrompts
    

#def initNewImageConvo():

def initTopSeller(sitekey, userId):
    filter = get_personalised_filter(sitekey, userId)
    top_query_brewer_response = top_query_brewer_client(filter)
    botResponsePrompts = BotResponsePrompts(products=top_query_brewer_response)
    print(botResponsePrompts.products)
    return botResponsePrompts

def get_personalised_filter(sitekey, userId):
    facets, var_facets = reranker_client(sitekey, userId)
    print(facets, var_facets)
    filter = []
    for facet in facets:
        if facet in affinity:
            filter.append(facet + ':' + list(affinity[facet].keys())[0])
    for var_facet in var_facets:
        if var_facet in affinity:
            filter.append(facet + ':' + list(affinity[var_facet].keys())[0])
    
    filter = ','.join(filter)
    print(filter)
    return filter

def initRFU(sitekey, userId):
    filter = get_personalised_filter(sitekey, userId)
    brewer_response = brewer_client(filter)
    botResponsePrompts = BotResponsePrompts(products=brewer_response)
    print(brewer_response)
    return botResponsePrompts

    
#def initTrending():

def initRedis(convo_id,userId, sitekey):
    redis_value = r.get(f'{userId}')
    json_str = redis_value.decode()
    val = json.loads(json_str)
    if convo_id in val:
        langchain_history = val[convo_id]['langchain_object']
    existingLangChainModel(langchain_history)



#checks for number of entries in redis for the uid, removes 1 if 3 is there and then adds new.
#Will add new entry by default if non exists
def update_redis_entries(redis_value, convo_id, data):
    if redis_value:
        json_str = redis_value.decode()
        val = json.loads(json_str)
        if len(val) == REDIS_ENTRIES:
            val = delete_convo_id(val)
        else:
            val = add_convo_id(val, convo_id, data)
    return val
            

def delete_convo_id(val):
    oldest_key = min(val, key=lambda k: val[k]['ts'])
    del val[oldest_key]
    return val

def add_convo_id(val, convo_id, data):
    convo_data = {
        convo_id: {
            'ts': int(datetime.now().timestamp()),
            'langchain_object': data
        }
    }

    val.update(convo_data)
    return val

