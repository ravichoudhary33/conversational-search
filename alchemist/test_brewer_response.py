import requests, json
from pydantic import BaseModel, parse_obj_as
from typing import List

boost_value = 100

class Product(BaseModel):
    title: str
    imageUrl: List[str]
    listPrice: str
    salePrice: str


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
    url = f'http://search.unbxd.io/b3094e45838bdcf3acf786d57e4ddd98/express_com-u1456154309768/search?q={query}&fields=title,imageUrl,listPrice,salePrice'
    for filter in fltrs:
        url =  url + f'&filter={filter}' + f'&bq={filter}^{boost_value}'

    resp = {'products':[]}
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
    data = json_data

    for pdt in data['response']['products']:
        product = parse_obj_as(Product, pdt)
        resp["products"].append(product)

    print(resp)

    return resp

model_brewer_client('suits', {
    "filter": {
        "sortPrice": "[* TO 50]",
        "categoryType_uFilter": "suits",
        "size_uFilter": "XL"
    }
})