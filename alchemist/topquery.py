import requests, json

url = 'http://aggregator.unbxdapi.com/analytics-aggregator/query-stats/express_com-u1456154309768/top-queries?fromDate=2023-01-01&toDate=2023-03-31&wt=json&limit=100'
response = requests.get(url)
print(response)

if response.status_code == 200:
    json_data = response.json()


#print(json_data)


queries = json_data['QueryStatResponse']['QueryStats']

top_queries = []
for q in queries:
    top_queries.append(q["query"])

print(top_queries)
