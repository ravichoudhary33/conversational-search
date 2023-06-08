from langchain.tools import BaseTool
import typing

from vector_store import RedisProductRetriever

class RetrievalTool(BaseTool):
    name = "Retrieve products"
    description = """use this tool when the user provides a search query or is searching for some products in a e-commerce store. 
    Return as much information as possible to the user including price, color, brand information"""
    redis_product_retriever = RedisProductRetriever()

    def _run(self, query: str):
        results = self.redis_product_retriever.get_relevant_documents(query)
        context = "\n".join([document.page_content for document in results])
        print(context)
        return context

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")