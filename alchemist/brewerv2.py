import requests
import json

pids = ["06419035", "06507794"]
scores = ["6183.213213","21763.3122"]
q = "parentId:("
counter = 0
for pid in pids:
    if counter == 0:
        q = q + f"\"{pid}\""
        counter += 1
    else:
        q = q + " OR " + f"\"{pid}\""
q = q + ")"

bf = "fieldcompare(parentId,\"{\\\"boostData\\\":{"
ub = "{\"boostData\":{"

for ind in range(len(pids)):
    if ind == 0:
        bf = bf + f"\\\"{pids[ind]}\\\":{scores[ind]}"
        ub = ub + f"\"{pids[ind]}\":{scores[ind]}"
    else:
        bf = bf + "," + f"\\\"{pids[ind]}\\\":{scores[ind]}"
        ub = ub + "," + f"\"{pids[ind]}\":{scores[ind]}"
bf += "}}\")"
ub += "}}"

print(q)
print(bf)
print(ub)

url = "http://brewer.prod.use-1d.infra/v2.0/sites/express_com-u1456154309768/search"

# Define the JSON body with customizable parameters
data = {
    "q": f"{q}",
    "start": "0",
    "boosts": [],
    "facets": [],
    "bf": [
        f"{bf}"
    ],
    "boost": [],
    "params": {
        "activeExperiment": {
            "values": ["false"]
        },
        "bq": {
            "values": ["sortPrice^100", "size_uFilter^100"]
        },
        "analysis": {
            "values": ["false"]
        },
        "asterix": {
            "values": ["false"]
        },
        "debug": {
            "values": ["true"]
        },
        "debug.structured": {
            "values": ["true"]
        },
        "dimension": {
            "values": ["false"]
        },
        "docstore": {
            "values": ["false"]
        },
        "fallback": {
            "values": ["false"]
        },
        "mimir.debug": {
            "values": ["true"]
        },
        "ner": {
            "values": ["false"]
        },
        "original.q": {
            "values": ["iphone"]
        },
        "promotion": {
            "values": ["false"]
        },
        "promotion.modifiedQuery": {
            "values": ["*"]
        },
        "qcs": {
            "values": ["false"]
        },
        "qis": {
            "values": ["false"]
        },
        "query.trim": {
            "values": ["false"]
        },
        "reranker.affinity.facet": {
            "values": ["false"]
        },
        "reranker.recommend": {
            "values": ["false"]
        },
        "reranker.rerank": {
            "values": ["false"]
        },
        "spellcheck.q": {
            "values": ["iphone"]
        },
        "ub.map": {
            "values": [f"{ub}"]
        },
        "useQisResponse": {
            "values": ["false"]
        }
    }
}

# Make the POST request
response = requests.post(url, json=data)

# Print the response
print(response.status_code)
print(response.json())
    

