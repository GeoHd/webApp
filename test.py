import requests
from flask import jsonify

route = "http://127.0.0.1:5000/"
response = requests.get(route+"api/polls/")
print(response.text)
"""

response = requests.post(route+"api/polls/",json={'question':'What is your favourite color?','answers_list':['Blue','Green','Yellow','Red']})
print(response.text)


response = requests.put(route+"api/poll/628d45fc809aed0f89dd6371",json={'vote':'Red'})
print(response.content)


response = requests.put(route+"api/poll/628d45fc809aed0f89dd6371",json={'vote':'Green'})
print(response.text)




response = requests.get(route+"api/poll/628d45fc809aed0f89dd6371")
print(response.text)
"""