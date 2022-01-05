import requests
from requests.models import Response

BASE = "http://127.0.0.1:5000/"

data = [
    {"likes": 10, "name": "study flask API", "views": 600},
    {"likes": 28, "name": "study vue.js", "views": 80000},
    {"likes": 91, "name": "study design sprint", "views": 7318}
]

for i in range(len(data)):
    response = requests.put(BASE + f"video/{i}", data[i])
    print(response.json())

input()
response = requests.get(BASE + "video/100")
print(response.json())