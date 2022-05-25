# webApp: code challange
## Author: George Hadib

# Intro:
webApp is a backend arquitecture for a polling sevice's webapp. The service uses a mongodb database called cisco and saves the polls into documents alocated in a collection called Polls and a python RESTful api server that connects to the database through pymongo

##################################################################

# Requirements:
Please make sure to fulfil the following requirements before testing the program:
1. Please make sure to have a mongodb server installed and configured in your local machine. For instant use of the program, make sure to run the server on localhost and port 27017. You can also adabt the code easily to environment changes by modifying the mongodb connector.
2. Please make sure to have python3 installed in your machine (built on python 3.8).
3. Please make sure to install the following python3 packages: flask, pymongo, bson, ast & requests

`python3 -m pip install [package_name]`


After fulfilling the requirements, you can run the mongodb database, run server and afterwards the test program. The test program will print the test cases and their results in the command line. Note that the server will run on localhost port 5000 por default.

##################################################################

# Methods:
## GET all database polls:
You can invoke this method by sending a GET request to the following url:

`http://127.0.0.1:5000/api/polls/`
This request will return a json file with all the polls in the database with the following format:

`{'Poll_1':{'_id':id, 'question': question_1, 'answers_list': answers_list_1}, 'Poll_2':{ ....}}`

##################################################################

## POST a new poll in the database:
You can invoke this mnethod by sending a POST request to the following url:

`http://127.0.0.1:5000/api/polls/`
The request should also contain a json payload with a similar format to the one below:

`{'question':'What is your favourite color?',
  'answers_list':['Blue',
                  'Green',
                   'Yellow',
                   'Red']}`

Please note that any type or key violations will result in a request failure.
A correctly created poll will return a json file containing the id of the poll in the database with the following format:

`{"poll_id":id}`

##################################################################

## GET one poll:
To use this method you should have a valid poll id to pass it as a parameter in the request. You can invoke this method by sending a GET request to the following url:

`http://127.0.0.1:5000/api/poll/+VALID_ID`

This request will return a json with the following format:

`{'_id':id, 'question': question, 'answers_list': answers_list}`

##################################################################

## PUT one answer:
To use this method you should have a valid poll id to pass it as a parameter in the request. You shold also send a payload answer with the following format:

`{'vote':VALID_ANSWER}`

Please note that valid answers are only the ones included in the poll when created

You can invoke this request by sending a PUT request to the following url:

`http://127.0.0.1:5000/api/poll/+VALID_ID`

Please note that any violation of the mentioned conditions will produce a failer
This request will return a json with the following format:

`{'_id':id, 'question': question, 'answers_list': new_answers_list}`

##################################################################

# Limitations:
1. No authentication method was used. A token generator can be used to allow creators to modify polls, users to change their answers and prevent users from answering multiple times
2. No deletion method es used. For the moment, creators can't delete their polls nor users their answers.
3. Only unique answers are accepted
4. No administrator figure is defined. An admin should be defined with some privileged methods.
5. Many other implementation limitations regarding security, access control, logging ...

##################################################################

Cheers!
