import json
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.redis import Redis as RedisVectorStore

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

def createVectorStore(NUMBER_PRODUCTS=1000):
    file = "express_com-u1456154309768-[1686213365723015437]--[3bd1ed46-1d87-4fa8-9775-bf30e4b177fc]-express_com-u1456154309768_2023_06_08_08_35_38_data_products.json"
    with open(file) as f:
        feed_data = json.load(f)
    
    # get the feed data
    feed_data = feed_data["feed"]["catalog"]["add"]["items"]
    # select few fields only
    fields = ["title","imageUrl","listPrice","salePrice","description", "brands", "gender", "categoryType", "color"]
    all_prods_df = pd.DataFrame(feed_data)[fields].copy()
    all_prods_df["item_name"] = all_prods_df['title'].astype(str) +". "+ all_prods_df["description"]

    # Get the first 2500 products
    product_metadata = ( 
        all_prods_df
        .head(NUMBER_PRODUCTS)
        .to_dict(orient='index')
    )

    # data that will be embedded and converted to vectors
    texts = [
        v['item_name'] for k, v in product_metadata.items()
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
    return vectorstore