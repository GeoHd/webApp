from asyncore import poll
from telnetlib import STATUS
import requests,ast

route = "http://127.0.0.1:5000/"


def post_insert(poll):
    response = requests.post(route+"api/polls/",json=poll)
    return (response)


def get_poll (id):
    response = requests.get(route+"api/poll/"+id)
    return (response)

def put_answer (id,answer):
    response = requests.put(route+"api/poll/"+id,json=answer)
    return(response)
    
def get_polls ():
    response = requests.get(route+"api/polls/")
    return (response)


def automated_test():
    print("\n************Start Testing************\n")
    

    print("Test 1:\nIn this test case we insert a correctly constructed poll.")
    good_poll = {'question':'What is your favourite color?','answers_list':['Blue','Green','Yellow','Red']}
    response = post_insert (good_poll)
    status = "Fail"
    response_text = response.content.decode()
    if (response.status_code==201):
        status = ">>Pass<<"
    print("Status: "+status)

    print("\n**************************************\n")
    
    print("Test 2:\nIn this test case we insert a poll with an empty question field..")
    bad_poll = {'question':'','answers_list':['Johnny Depp','Amber Heard','Amber Heard\'s lawyer']}
    response = post_insert (bad_poll)
    status = ">>Pass<< | The server refuses to create the new poll and returns the status code: "+ str(response.status_code)+" and the following message:\n\n"+response.content.decode()
    if (response.status_code==201):
        status = "Fail"
    print("Status: "+status)
    print("\n**************************************\n")


    print("Test 3:\nIn this test case we insert a poll with an empty answers' list..")
    bad_poll = {'question':'Who is your bes UCL player?','answers_list':[]}
    response = post_insert (bad_poll)
    status = ">>Pass<< | The server refuses to create the new poll and returns the status code: "+ str(response.status_code)+" and the following message:\n\n"+response.content.decode()
    if (response.status_code==201):
        status = "Fail"
    print("Status: "+status)

    print("\n**************************************\n")


    print("Test 4:\nIn this test case we answer an existant poll with a valid answer..")
    poll_id = ast.literal_eval(response_text)["poll_id"]
    
    valid_answer = {'vote':'Red'}

    response = put_answer (poll_id,valid_answer)

    status = "Fail"
    if (response.status_code==200):
        status = ">>Pass<< | You answer was added successfully to the poll.."
    print("Status: "+status)
    print("\n**************************************\n")


    print("Test 5:\nIn this test case we answer an existant poll with a invalid answer..")
    
    invalid_answer = {'vote':'Johnny Depp'}

    response = put_answer (poll_id,invalid_answer)

    status = ">>Pass<< | The server fails to add the answer to the poll and returns the status code: "+ str(response.status_code)+" and the following message:\n\n"+response.content.decode()
    if (response.status_code==200):
        status = "Fail"
    print("Status: "+status)
    print("\n**************************************\n")

    print("Test 6:\nIn this test case we try to answer an non-existant poll..")
    
    invalid_answer = {'vote':'Johnny Depp'}

    response = put_answer ("try_this_id",invalid_answer)

    status = ">>Pass<< | The server fails to find the poll and returns the status code: "+ str(response.status_code)+" and the following message:\n\n"+response.content.decode()
    if (response.status_code==200):
        status = "Fail"
    print("Status: "+status)
    print("\n**************************************\n")
    print("Test 7:\nIn this test case we request the information of an existing poll")
      
    response = get_poll(poll_id)

    status = "Fail"
    if (response.status_code==200):
        status = ">>Pass<< | The server returns the information of the poll in a json format"
    print("Status: "+status)
    print("\n**************************************\n")
    print("Test 8:\nIn this test case we request the information of a non-existing poll")
      
    response = get_poll("this_pol_doesn't exist")

    status = ">>Pass<< | The server fails to find the poll and returns the status code: "+ str(response.status_code)+" and the following message:\n\n"+response.content.decode()
    if (response.status_code==200):
        status = "Fail"
    print("Status: "+status)
    print("\n**************************************\n")

    print("Test 9:\nIn this test case we request the information of all the polls in the database")
      
    response = get_polls()

    status = "Fail"
    if (response.status_code==200):
        status = ">>Pass<< | The server responds with a json file with all the polls in the database"
    print("Status: "+status)   
    print("\n************Finish Testing************\n")


automated_test()
