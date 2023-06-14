import openai
import re
import json
from brewer_fake import fake_filters, fake_prods
from schemas import Product
from pydantic import parse_obj_as
from typing import List
import requests
import ast


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


facet_resp = get_completion(relevant_facet_prompt)
print(f"The returned facet resp ayush check: {facet_resp}")