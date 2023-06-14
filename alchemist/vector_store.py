import json
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.redis import Redis as RedisVectorStore
import openai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

#
# from langchain.schema import BaseRetriever
# from langchain.vectorstores import VectorStore
# from langchain.schema import Document
# from pydantic import BaseModel
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores.redis import Redis as RedisVectorStore
#
#
# class RedisProductRetriever(BaseRetriever, BaseModel):
#     vectorstore: VectorStore = None
#
#     def create_vector_store(cls):
#         file = "express_com-u1456154309768-[1686213365723015437]--[3bd1ed46-1d87-4fa8-9775-bf30e4b177fc]-express_com-u1456154309768_2023_06_08_08_35_38_data_products.json"
#         with open(file) as f:
#             feed_data = json.load(f)
#
#         feed_data = feed_data["feed"]["catalog"]["add"]["items"]
#
#         texts = [item.get("description", item.get("productDescription", "No description found")) for item in feed_data]
#
#         # product metadata that we'll store along our vectors
#         # metadatas = list(product_metadata.values())
#         metadatas = feed_data
#
#         # we will use OpenAI as our embeddings provider
#         embedding = OpenAIEmbeddings()
#
#         # name of the Redis search index to create
#         index_name = "products"
#
#         # assumes you have a redis stack server running on within your docker compose network
#         redis_url = "redis://redis:6379"
#
#         cls.vectorstore = RedisVectorStore.from_texts(
#             texts=texts,
#             metadatas=metadatas,
#             embedding=embedding,
#             index_name=index_name,
#             redis_url=redis_url
#         )
#
#     class Config:
#         arbitrary_types_allowed = True
#
#     def combine_metadata(self, doc) -> str:
#         metadata = doc.metadata
#         metadata_dict = {
#             "Product ID:": metadata.get("uniqueId", ""),
#             "Product Title:": metadata.get("title", ""),
#             "Product Color:": metadata.get("color", ""),
#             "Product Price:": metadata.get("selling_price", ""),
#             "Product Brands:": metadata.get("brands", ""),
#             "Product Image URL:": metadata.get("productImage", ""),
#             "Product URL:": metadata.get("productURL", ""),
#             "Product Description:": metadata.get("description", "")
#         }
#         return json.dumps(metadata_dict)
#
#     def get_relevant_documents(self, query):
#         docs = []
#         for doc in self.vectorstore.similarity_search(query):
#             content = self.combine_metadata(doc)
#             docs.append(Document(
#                 page_content=content,
#                 metadata=doc.metadata
#             ))
#         return docs

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_completion(prompt,model="gpt-3.5-turbo"):  # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def get_product_specs_prompt(json_string):
    prompt = f"""
        Your task is to generate a more informative summary of a product \
        using it's specification from an ecommerce site \
        pricing deparmtment, responsible for determining the \
        price of the product.  

        Summarize the product below, delimited by triple 
        backticks, in at most 30 words, and focusing on any aspects \
        that are relevant to the color, gender, price and perceived value. 

        Product Specification: ```{json_string}```
    """
    response = get_completion(prompt)
    return response

def createVectorStore(NUMBER_PRODUCTS=100, use_summary = False):
    file = "express_com-u1456154309768-[1686213365723015437]--[3bd1ed46-1d87-4fa8-9775-bf30e4b177fc]-express_com-u1456154309768_2023_06_08_08_35_38_data_products.json"
    with open(file) as f:
        feed_data = json.load(f)
    
    # get the feed data
    feed_data = feed_data["feed"]["catalog"]["add"]["items"]
    # select few fields only
    fields = ["title","imageUrl","listPrice","salePrice","description", "brands", "gender", "categoryType", "color"]
    all_prods_df = pd.DataFrame(feed_data)[fields].copy()

    if use_summary:
        all_prods_df["item_summary"] = all_prods_df.apply(lambda x: get_product_specs_prompt(json.dumps(dict(x))), axis=1)
    else:
        all_prods_df["item_summary"] = all_prods_df['title'].astype(str) +". "+ all_prods_df["description"]

    # store the df for debugging
    # all_prods_df.to_csv('./all_prods_df.csv', ignore_index=True)

    # Get the first NUMBER_PRODUCTS
    product_metadata = ( 
        all_prods_df
        .head(NUMBER_PRODUCTS)
        .to_dict(orient='index')
    )

    # data that will be embedded and converted to vectors
    texts = [
        v['item_summary'] for k, v in product_metadata.items()
    ]
    
    # product metadata that we'll store along our vectors
    metadatas = list(product_metadata.values())

    # create the vector store
    embedding = OpenAIEmbeddings()
    # name of the Redis search index to create
    index_name = "products_v2"
    # assumes you have a redis stack server running on within your docker compose network
    redis_url = "redis://redis:6379"
    # create and load redis with documents
    vectorstore = RedisVectorStore.from_texts(
        texts=texts,
        metadatas=metadatas,
        embedding=embedding,
        index_name=index_name,
        redis_url=redis_url
    )
    # store the vectorstore locally
    # vectorstore.save_local('./local_vectorstore')
    return vectorstore