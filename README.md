# webApp: code challange
## Author: George Hadib

# Intro:
webApp is a backend arquitecture for a polling sevice's webapp. The service uses a mongodb database called cisco and saves the polls into documents alocated in a collection called Polls and a python RESTful api server that connects to the database through pymongo

# Requirements:
Please make sure to fulfil the following requirements before testing the program:
1. Please make sure to have a mongodb server installed and configured in your local machine. For instant use of the program, make sure to run the server on localhost and port 27017. You can also adabt the code easily to environment changes by modifying the mongodb connector.
2. Please make sure to have python3 installed in your machine (built on python 3.8).
3. Please make sure to install the following python3 packages: flask, pymongo, bson, ast & requests

`python3 -m pip install [package_name]`


After fulfilling the requirements, you can run the mongodb database, run server and afterwards the test program. The test program will print the test cases and their results in the command line.

# Limitations:
1. No authentication method was used. A token generator can be used to allow creators to modify polls, users to change their answers and prevent users from answering multiple times
2. No deletion method es used. For the moment, creators can't delete their polls nor users their answers.
3. No administrator figure is defined. An admin should be defined with some privileged methods.
4. Many other implementation limitations regarding security, access control, logging ...

Cheers!
