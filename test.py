import requests
from flask import jsonify

route = "http://127.0.0.1:5000/"

response = requests.post(route+"api/polls/",json={'question':'This is a question','answers_list':['answer_1','answer_2','answer_3']})
print(response._content)