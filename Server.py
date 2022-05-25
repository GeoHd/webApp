from flask import Flask, request, Response 
from flask_restful import Api, Resource
from pymongo import MongoClient, ReturnDocument 
from bson.objectid import ObjectId
import os,ast

# Configure the mongodb connector
# Important: Please make sure that the host name and the port matchs the ones of your mongodb server
mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)    #Configure the connection to the database
db = client.cisco    # Select the database
poll_col = db["Polls"] # Select the collection

# Start the flask API app
app = Flask(__name__)
api = Api(app)


# This class is used for requests that have entry queries such as get all the polls in the database and post a new poll
class Polls (Resource):
    # This method recieves no parameters and returns all the polls in the database
    # It basically brings every poll in the database, does some casting and returns a dictionary with all of them
    def get(self):
        try:
            results=list(poll_col.find({}))
            results_str = str(results)
            results_clean = results_str.replace("ObjectId(","").replace(")","")
            results_clean_list = ast.literal_eval(results_clean)
            results_dict = {}
            i=1

            for poll in results_clean_list:
                results_dict["Poll "+str(i)]=poll
                i+=1
 #           
            return Response(str(results_dict), status=200,mimetype="application/json")


        except:
            return Response("Service is not available right now. Please try again soon..",status=500, mimetype="application/json")

    # This method recieves a payload in json format and creates a new poll in the database
    # A format check is carried on and respective error messages and status codes are returned
    # In case of a successful operation, it returns a json file that contains the id of the poll
    # It can be adapted easily to return the full poll but in this case, an id was good enough
    def post(self):

        try:
            dictionary = dict(request.get_json())
            answers_list = {}
            for answer in  list(dictionary.get('answers_list')):
                answers_list[answer]=0
            new_entry = {'question':str(dictionary.get('question')),'answers_list':answers_list}
            
    
            # Empty or non-existent question field?    
            if (len(new_entry.get('question'))==0):
                return Response("Bad entry! Your question field looks empty..",status=400, mimetype="application/json")
            # Empty or non-existent answers field?    
            elif (len(new_entry.get('answers_list'))==0):
                return Response("Bad entry! Please make sure to add some answers to your poll..",status=400, mimetype="application/json")
            
                
            # Correct formant >> create in database
            result = poll_col.insert_one(new_entry)
            
            id = result.inserted_id
            
            response_text =   str({"poll_id":id})  
            response_text = response_text.replace("ObjectId(","").replace(")","")
            return Response(response_text,status=201, mimetype='application/json')
            
        except:

            return Response("Bad entry! Please make sure that the entry match the especification in the documentation",status=400, mimetype="application/json")





# This class is used for operations on existant polls.. It recieves a id query
class Poll (Resource):

    # This method searchs for the id in the database and returns the whole poll
    # Some casting and adaptation are needed
    # If the id doesn't exist in the database or if there is any type violations it returns an error message with the proper status code
    def get(self,id):
        try:
            poll_dict = str(poll_col.find_one(ObjectId(id)))
            
            if (poll_dict!=None):
                poll_dict =ast.literal_eval(poll_dict.replace("ObjectId(","").replace(")",""))
                
                return Response(str(poll_dict),status=200,mimetype= 'application/json')
            else:
                return Response("Bad entry! Please make sure to enter a valid poll id",status=404,mimetype="application/json")
        except:
            return Response("Bad entry! Please make sure to enter a valid poll id",status=404,mimetype="application/json")
        

    # This method answers a poll
    # Two diferent error checks, one for the existance of the poll and the other one is for the validity of the answer
    # Proper error messages and status codes are returned
    def put(self,id):
        try:
            dictionary = dict(request.get_json())
            chosen_answer = list(dictionary.values())[0]
            poll_dict = str(poll_col.find_one(ObjectId(id)))
            poll_dict =ast.literal_eval(poll_dict.replace("ObjectId(","").replace(")",""))
            
            answers_list = poll_dict["answers_list"]
            if chosen_answer in answers_list:
                answers_list[chosen_answer]+=1
                
                poll_dict["answers_list"]=answers_list
                poll_col.find_one_and_update(filter={"_id":ObjectId(id)},update={'$set':{"answers_list":answers_list}},return_document=ReturnDocument.AFTER)
                return Response(str(poll_dict),status=200,mimetype='application/json')
            else:
                return Response("Bad entry! Please make sure to enter a valid answer",status=400,mimetype="application/json")

        except: 
            return Response("Bad entry! Please make sure to enter a valid poll id",status=404,mimetype="application/json")



  
# Adding those resources
api.add_resource(Poll,"/api/poll/<string:id>")
api.add_resource(Polls,"/api/polls/")






# Execution

if __name__ == "__main__":
    app.run(debug=True)



