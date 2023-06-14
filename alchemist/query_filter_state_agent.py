import openai
import re
import json
from brewer_fake import fake_filters, fake_prods
from schemas import Product
from pydantic import parse_obj_as
from typing import List
import requests
import ast
# from vector_store import RedisProductRetriever


class QueryFilterStateAgent():
    context_v2 = [{'role': 'system', 'content': f"""
            You are an AI assistant for an e-commerce platform and help the user find the relevant product, based on user query. \
            Refrain from apologizing unnecessarily. \
            You are an automated service to collect requirements for a product. \
            You first greet the customer, then collects the requirement, \
            and then ask if the user like to add to the cart. \
            You wait to collect the entire requirement, then summarize it and check for a final \
            time if the customer wants to add anything else. \
            Finally, you collect the payment.\
            Make sure to clarify all options, extras and sizes uniquely. \
            At each step, based on chat history, you maintain current query the user is looking for and filters that can go along with it. \
            Filters can include attributes like color, size, brand, material etc. \
            Eg if user searches for red sports shoes, query will be red sports shoes and filters will be {{"color": "red"}} \
            You respond in a short, very conversational friendly style. \
            """}]  # accumulate messages
    
    context = [{'role': 'system', 'content': f"""
            You are an AI assistant for an e-commerce platform and help the user find the relevant product, based on user query. \
            Identify the user gender as the conversation goes on.\
            While giving the user preferenence keep that in mind. \
            You are an automated service to collect requirements for a product. \
            You first greet the customer, then collects the requirement, \
            and then ask if the user like to add to the cart. \
            You wait to collect the entire requirement, then summarize it and check for a final \
            time if the customer wants to add anything else. \
            Finally, you collect the payment.\
            Make sure to clarify all options, extras and sizes uniquely. \
            You respond in a short, very conversational friendly style. \
            """}]  # accumulate messages


    autosuggest_context = [{'role': 'system', 'content': f"""
            You are a query suggestion platform for apparel vertical ecommerse site. \
            Use the provided context to suggest short and accurate query suggestion only.\
            Do not user more then 15 characters.\
            Format the output as a JSON object with only keys as auto_suggestions without any additional text.\
            Make sure auto_suggestions list does not have more than 4 elements.\
            Wrap the output with triple backticks.\
            Here's an example of the expected output format:\
            ```{{
                "auto_suggestions": [suggestion_first, suggestion_second, ...]
            }}```
            """}]  # accumulate messages

    summary_context = [{'role': 'system', 'content': f"""
                You are a product description summarizer for apparel vertical ecommerse site. \
                Given product attributes for list of products, generate a concise summary.\
                Don't use product URL or product score for the summary.\
                """}]  # accumulate messages


    def __init__(self):
        self.convo_history = {}
        # self.productRetriever = RedisProductRetriever()
        # self.productRetriever.create_vector_store()
        

    def get_completion_from_messages(self, messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message["content"]

    def get_completion(self, prompt,
                       model="gpt-3.5-turbo"):  # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,  # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]

    def extract_imp_info(self, response):
        imp_response = re.findall(r'"([^"]*)"', response)
        if imp_response:
            imp_response = imp_response[0]
        return imp_response

    def get_solr_filters(self, query):
        solr_prompt = f"""
        given the list of filters: delimited by triple backticks. Filters: ```["length_uFilter", "color_uFilter", \
        "fit_uFilter", "sortPrice", "size_uFilter", "categoryType_uFilter", \
        "type_uFilter", "gender_uFilter", "legShape_uFilter", "sleeveLength_uFilter",\
        "occasion_uFilter", "styleRefinement_uFilter", "rise_uFilter"]``` and given constrainst: ```{query}```. Identify list of \
        solr filter among the Filters find value corresponds to the the given constraints. \
        If its a filter like under/over/between, write values fqs that are range solr queries. Return output in  json object only. \
        with keys as "filter" and it's value should contain all the solr fqs. Do not invent your own uFilters apart from the ones provided. User sortPrice:[min TO max] for range filters on price.\

        """

        res = self.get_completion(solr_prompt)
        # print(res)
        try:
            res = eval(res)
        except Exception as e:
            res = ""
        return res

    def parse_content_inside_backticks(self, string):
        pattern = r"```([\s\S]*?)```"
        matches = re.findall(pattern, string, re.DOTALL)
        # data = json.loads(matches[0].replace('\n', ''))
        return matches

    def parse_autosuggest_response(self, autosuggest_response):
        autosuggestions = self.parse_content_inside_backticks(autosuggest_response)
        try:
            return json.loads(autosuggestions[0])["auto_suggestions"]
        except Exception as e:
            print("Exception", e)
            return []

    def parse_prods(self, products):
        products = eval(products)['products']
        products = [{"title": product["titile"], "image_url": product["imageUrl"], "last_price": product["list_price"], "sale_price": product["salePrice"]} for product in products]
        return products

    def fetch_products(self, query, filters):
        query = query.replace("'", '').replace('"', '').replace('.', '').replace('!', '').replace('?', '')

        # with open('affinity.json') as file:
        #     affinity = json.load(file)
        #     #print(affinity)
        # express_top_facets = ["length_uFilter", "color_uFilter", "fit_uFilter", "sortPrice", "size_uFilter", "categoryType_uFilter", "type_uFilter", "gender_uFilter", "legShape_uFilter", "sleeveLength_uFilter", "occasion_uFilter", "styleRefinement_uFilter", "rise_uFilter"]
        # json_data1 = {
        #     "userId": "uid-1683602268183-16966",
        #     "facetAffinity": {},
        #     "msTaken": 42
        # }
        # data = json_data1
        # facetAffinity = data['facetAffinity']
        # facets = []
        # if len(facetAffinity)<4:
        #     for facet in express_top_facets:
        #         if facet not in facets:
        #             facets.append(facet)
        #         if len(facets)==4:
        #             break

        # print("my facet : ",facets)
        # filter = []
        # for facet in facets:
        #     if facet in affinity:
        #         filter.append(facet + ':' + list(affinity[facet].keys())[0])
        
        # if len(filter)>=4:
        #     filter = filter[:4]
        # filter = ','.join(filter)

        # print("my filter : ",filter)
        fields = "title,imageUrl,listPrice,salePrice,score,description"
        if filters:
            url = f'http://search.unbxd.io/b3094e45838bdcf3acf786d57e4ddd98/express_com-u1456154309768/search?q={query}&fields={fields}'
            for filt in filters:
                url = url + f'&bq={filt.split(":")[0]}^{100}'
        else:
            url = f'http://search.unbxd.io/b3094e45838bdcf3acf786d57e4ddd98/express_com-u1456154309768/search?q={query}&fields={fields}'
        
        response = requests.get(url)

        resp = []
        print(url, response.status_code)
        if response.status_code == 200:
            json_data = response.json()

            pdts = json_data['response']['products']
            # print(pdts)
            for data in pdts:
                # print(data)

                product = {field: data[field] for field in fields.split(",")}

                resp.append(product)
            resp = sorted(resp, key=lambda x: x.get("score", 0), reverse=True)
        return resp

    def get_facets(self, user_id):
        url = f"http://reranker.prod.use-1d.infra/v1.0/sites/express_com-u1456154309768/affinity/facet?userId={user_id}"
        print(url)

        json_data = {}
        try:
            response = requests.get(url)
            if response.status_code == 200:
                json_data = response.json()
            else:
                print("response status code from reranker:", response.status_code)
        except:
            with open("affinity-response.json") as f:
                json_data = json.load(f)
        return json_data

    def collect_message(self, user_id, human_input):
        if user_id in self.convo_history:
            user_context = self.convo_history[user_id]["context"]
            user_autosuggest_context = self.convo_history[user_id]["autosuggest_context"]
        else:
            pers_facets = self.get_facets(user_id)

            self.convo_history[user_id] = {}
            user_context = self.context
            if len(pers_facets) > 10:
                user_context[0]["content"] += "The following facets determine the likes, dislikes and personality " \
                    "of the user. Higher score for a field indicates stronger interest of the user. The facets are " + \
                    json.dumps(pers_facets)
            print(user_context)
            self.convo_history[user_id]["context"] = user_context
            user_autosuggest_context = self.autosuggest_context
            self.convo_history[user_id]["autosuggest_context"] = user_autosuggest_context

        user_context.append({'role': 'user', 'content': f"{human_input}"})
        response = self.get_completion_from_messages(user_context)
        user_context.append({'role': 'assistant', 'content': f"{response}"})

        #### Comment logic for finding filter and query
        # user_context.append({'role': 'user',
        #                 'content': "What is my Current query? Return only the search query. Do not print anything else but the search query. No extra words."})
        # query_response = self.get_completion_from_messages(user_context)
        # query = self.extract_imp_info(query_response)
        # user_context = user_context[:-1]
        # print("Current query:", query_response)
        # print(query)
        # user_context.append({'role': 'user',
        #                 'content': "What are my Current filters? Print only the current filters in json format and nothing else. No extra words"})
        # filter_response = self.get_completion_from_messages(user_context)
        # filters = self.extract_imp_info(filter_response)
        # if filters:
        #     filters = self.get_solr_filters(filters)

        # print("Current filters:", filter_response)
        # print(filters)
        # user_context = user_context[:-1]

        # summary_query_response = ""
        # parsed_showcase_products = []
        # if query:
        #     showcase_products = self.fetch_products(query, filters='')
        #     self.summary_context.append({'role': 'assistant', 'content': json.dumps(showcase_products)})
        #     summary_query_response = self.get_completion_from_messages(self.summary_context)
        #     self.summary_context = self.summary_context[:-1]
        #     print(summary_query_response)
        #     #user_context.append({'role': 'assistant', 'content': summary_query_response})

        #     parsed_showcase_products = [parse_obj_as(Product, showcase_product) for showcase_product in
        #                                 showcase_products]
        #     print(parsed_showcase_products)


        # get query suggestions response
        user_autosuggest_context.append({'role': 'user', 'content': f"{human_input}"})
        user_autosuggest_context.append({'role': 'assistant', 'content': f"{response}"})
        as_response = self.get_completion_from_messages(user_autosuggest_context)
        user_autosuggest_context.append({'role': 'assistant', 'content': f"{as_response}"})

        parsed_as_response = self.parse_autosuggest_response(as_response)


        ## based on the current respone figure out if it's a follow up question, else summaries the query
        # some variable to initialize
        summary_query_response = ""
        parsed_showcase_products = []
        f = []

        is_follow_up = f"""
            Given the query delimited by triple backticks. Return if the given query is a follow up \
            questions. Give your answer as either yes or no. For example if it's a greeting query then obviously \
            it's a follow up so in that case the answer should be yes.\
            Query text: ```{human_input}```
        """
        f_response = self.get_completion(is_follow_up)
        print(f"follow up query response: {f_response}")
        if len(f_response) > 0 and 'no' in f_response.lower():
            # means it's not a follow up so apply search query
            # if we are here then get the 
            convo_history = self.convo_history[user_id]["context"]
            print(f"Convo history till now: {convo_history[1:]}")
            compressed_query_prompt = f"""
                Given the chat history of the conversation delimited by triple backticks. Return the \
                small query containing the user requirements. and the suggested solr filters\
                Do not use more than 50 characters for the query and do not use repeated information.\
                The query should be non instructional.
                Chat History: ```{convo_history}```
                Return the output as a JSON object with two key with name condesensed_query and suggested_filters.\
                Sample Ouput is delimited by triple backticks:-
                ``` {{'condensed_query': <condensed query>, 'suggested_filters': <suggested filters> }}
            """
            new_query_resp = self.get_completion(compressed_query_prompt)
            print(f"The condensed query resp: {new_query_resp}")
            # get the products
            try:
                resp = eval(new_query_resp)
                f = []#resp['suggested_filters']
                q = resp['condensed_query']
            except:
                q = new_query_resp
                f = []
            print(f"resolved query: {q}")
            print(f"resolved filter: {f}")

            # given the query and the list of facet for that site give me most three relevant facet for that query
            relevant_facet_prompt = f""""
                Given a search query delimited by ``` and a list of filters delimited by ```, give me 3 most relevant filters for that query.
                Given Query:  ``` {q} ```
                Given Filters: ``` ["length_uFilter", "color_uFilter", "fit_uFilter", "sortPrice", "size_uFilter", "type_uFilter", "gender_uFilter", "legShape_uFilter", "sleeveLength_uFilter", "occasion_uFilter", "styleRefinement_uFilter", "rise_uFilter"] ```
                Return only the final output of filters as a list
                Sample output: ``` ["length_uFilter", "color_uFilter", "fit_uFilter"]
            """

            # with open('affinity.json') as file:
            #     affinity = json.load(file) 
            
            
            facet_resp = self.get_completion(relevant_facet_prompt)
            print(f"The returned facet resp ayush check: {facet_resp}")

            with open('affinity.json') as file:
                affinity = json.load(file)
            #print(affinity)

            pop_filters = []

            for facet in affinity:
                pop_filters.append(facet.keys()[0])

            facets = []
            for facet in list(facet_resp):
                if facet not in facets:
                    facets.append(facet)
                if len(facets)==4:
                    break

            print("my facet : ",facets)
            filter = []
            for facet in facets:
                if facet in affinity:
                    filter.append(list(affinity[facet].keys())[0])
            
            if len(filter)>=4:
                filter = filter[:4]

                filter = []
                for facet in facet_resp:
                    if facet in affinity:
                        filter.append(facet + ':' + list(affinity[facet].keys())[0])
            
            print(filter)
                

            showcase_products = self.fetch_products(query = q, filters=f)
            parsed_showcase_products = [parse_obj_as(Product, showcase_product) for showcase_product in
                                        showcase_products]


        all_resp = {
            'product_summary': summary_query_response,
            'assistant': response,
            'assistant_autosuggest_response': as_response,
            'suggested_queries': parsed_as_response,
            'suggested_filters': facet_resp if len(f) > 0 else [], #fake_filters("", ""),
            'products': parsed_showcase_products
        }

        return all_resp['product_summary'], all_resp['assistant'], all_resp['assistant_autosuggest_response'], all_resp['suggested_queries'], all_resp['suggested_filters'], all_resp['products']
