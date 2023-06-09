#from alchemist import RERANKER_HOST, RERANKER_NORM, REGION
import json, requests
from pydantic import BaseModel, parse_obj_as
from typing import List

regions = ['use-1d', 'ap-southeast-1', 'ap-southeast-2', 'eu-west-2']
express_top_facets = ["length_uFilter", "color_uFilter", "fit_uFilter", "sortPrice", "size_uFilter", "categoryType_uFilter", "type_uFilter", "gender_uFilter", "legShape_uFilter", "sleeveLength_uFilter", "occasion_uFilter", "styleRefinement_uFilter", "rise_uFilter"]
var_facets = ["v_color_uFilter", "v_size_uFilter", "v_color_ufilter", "v_length_uFilter"]
top_queries = ["Dress", "Blazer", "Bodysuit", "Jumpsuit", "Sequin", "Portofino", "Body contour", "Skirt", "Leggings", "Cardigan", "White dress", "Romper", "Women pants", "Shorts", "Cami", "Women jeans", "Women blazer", "Black dress", "Pants", "Body suit", "Sweater", "Corset", "Jeans", "Shoes", "Earrings", "Blouse", "Socks", "Maxi dress", "Tops", "Belt", "White jeans", "Editor", "Leather pants", "Vest", "Clearance", "Skyscraper", "Crop top", "Suit", "Leather", "Pink", "Neon berry", "Denim dress", "Coat", "Polo", "Sweater dress", "Satin", "Blazer dress", "Linen", "Floral", "Peplum", "Jacket", "Editor pants", "Pink dress", "Maternity", "White pants", "Joggers", "Heels", "Cargo pants", "Midi dress", "Tweed", "Hoodie", "Faux leather", "Floral dress", "Tank", "Cargo", "Portofino shirt", "Contour", "Tank top", "Wide leg pants", "Bright kelly", "Gramercy", "Tube top", "Flare jeans", "Sandals", "Black jeans", "White blazer", "Pink blazer", "Lemon yellow", "Duster", "Curvy", "Flexx", "Wide leg jeans", "One shoulder", "Lace", "Curvy jeans", "Trench coat", "White top", "Swim", "Bubble", "Wide leg", "Shirt dress", "Gum pop", "Bra cami", "Swan", "Rayon", "Purple", "Pink pants", "Orange", "Puff sleeve", "Halter"]
boost_value = 100

class Product(BaseModel):
    title: str
    imageUrl: List[str]
    listPrice: str
    salePrice: str

json_data1 = {
    "userId": "uid-1683602268183-16966",
    "facetAffinity": {
      "colorName_uFilter": {
        "White": 6.206193986078503,
        "Pitch Black": 100,
        "Pecan": 5.2947948692418,
        "Pale Yellow": 4.990995163629566,
        "Pink": 4.990995163629566
      },
      "categoryType_uFilter": {
        "Tops": 100,
        "Bottoms": 2.3961666921528346,
        "Sweaters": 1
      },
      "gender_uFilter": {
        "women": 100
      },
      "type_uFilter": {
        "Tanks": 9.00147275888102,
        "Pants": 6.1885125217307015,
        "Bodysuits": 100,
        "Sweaters": 1.0126656853741147,
        "Tees": 1
      }
    },
    "msTaken": 42
  }

def reranker_client(sitekey, userId):

    # responses.add(responses.GET, 'http://reranker.prod.use-1d.infra/v1.0/sites/express_com-u1456154309768/affinity/facet?userId=uid-1683602268183-16966&platform=realtime&norm=100', json=json_data1, status=200)
    # # url = 'http://0.0.0.0:12002/v1.0/sites/express_com-u1456154309768/affinity/facet?userId=uid-1683602268183-16966&platform=realtime&norm=100'
    # # print(url)
    # # response = requests.get(url)

    # # if response.status_code == 200:
    # #     json_data = response.json()
    # for region in regions:
    #     url = 'http://reranker.prod.' + region + '.infra/v1.0/sites/express_com-u1456154309768/affinity/facet?userId=uid-1683602268183-16966&platform=realtime&norm=100'
    #     print(url)
    #     response = requests.get(url)

    #     if response.status_code == 200:
    #         json_data = response.json()
    #         break
    #     else:
    #         continue
    
    # data = json.loads(json_data)
    data = json_data1
    facetAffinity = data['facetAffinity']
    facets = list(facetAffinity.keys())
    if len(facets)<4:
        for facet in express_top_facets:
            if facet not in facets:
                facets.append(facet)
            if len(facets)==4:
                break
    
    return facets, var_facets

def brewer_client(filter):
    url = 'http://search.unbxd.io/b3094e45838bdcf3acf786d57e4ddd98/express_com-u1456154309768/search?q=*'  + '&' + filter + '&fields=title,imageUrl,listPrice,salePrice&promotion=false'
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
    # for region in regions:
    #     url = 'http://brewer.prod.' + region + '.infra/b3094e45838bdcf3acf786d57e4ddd98/express_com-u1456154309768/search?q=*'  + '&' + filter + '&fields=productId,title,imageUrl,listPrice,salePrice'
    #     response = requests.get(url)

    #     if response.status_code == 200:
    #         json_data = response.json()
    #         break
    #     else:
    #         continue

    #data = json.loads(json_data)
    pdts = json_data['response']['products']
    resp = []
    for data in pdts:
        print(data)

        product = parse_obj_as(Product, data)
        resp.append(product)

    return resp
    

    
    
def top_query_brewer_client(filter):
    # reg = ""
    # for region in regions:
    #     url = 'http://brewer.prod.' + region + '.infra/b3094e45838bdcf3acf786d57e4ddd98/express_com-u1456154309768/search?q=*'
    #     response = requests.get(url)

    #     if response.status_code == 200:
    #         reg = region
    #         break
    #     else:
    #         continue
    
    resp = []
    counter = 0
    for top_query in top_queries:
        url = f'http://search.unbxd.io/b3094e45838bdcf3acf786d57e4ddd98/express_com-u1456154309768/search?q={top_query}&{filter}&fields=productId,title,imageUrl,listPrice,salePrice&rows=1&promotion=false'
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
        data = json_data

        data = data['response']['products'][0]
        product = parse_obj_as(Product, data)
        resp.append(product)
        counter+=1
        if counter == 10:
            break

    return resp

def model_brewer_client(query, filters):
    # reg = ""
    # for region in regions:
    #     url = 'http://brewer.prod.' + region + '.infra/b3094e45838bdcf3acf786d57e4ddd98/express_com-u1456154309768/search?q=*'
    #     response = requests.get(url)

    #     if response.status_code == 200:
    #         reg = region
    #         break
    #     else:
    #         continue
    filters = filters['filter']
    fltrs = []
    for k,v in filters.items():
        if k=='categoryType_uFilter':
            query = v
            continue
        fltrs.append(k+':'+v)
    print(fltrs)
    url = f'http://search.unbxd.io/b3094e45838bdcf3acf786d57e4ddd98/express_com-u1456154309768/search?q={query}&fields=title,imageUrl,listPrice,salePrice&promotion=false'
    for filter in fltrs:
        url =  url + f'&filter={filter}' + f'&bq={filter}^{boost_value}'
    
    resp = []
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
    data = json_data

    for pdt in data['response']['products']:
        product = parse_obj_as(Product, pdt)
        resp.append(product)
    
    print(resp)

    return resp

    

