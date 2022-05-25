
from asyncore import poll
from unittest import result
from flask import Flask, request, jsonify,Response # For flask implementation
from flask_restful import Api, Resource, abort
#import pymongo
from pymongo import MongoClient, ReturnDocument # Database connector
from bson.objectid import ObjectId
import os,ast


mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)    #Configure the connection to the database
db = client.cisco    #Select the database
poll_col = db["Polls"]


app = Flask(__name__)
api = Api(app)


class Polls (Resource):
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


    def post(self):
        try:
            dictionary = dict(request.get_json())
            answers_list = {}
            for answer in  list(dictionary.get('answers_list')):
                answers_list[answer]=0
            new_entry = {'question':str(dictionary.get('question')),'answers_list':answers_list}
            
    
            
            if (len(new_entry.get('question'))==0):
                return Response("Bad entry! Your question field looks empty..",status=400, mimetype="application/json")
            elif (len(new_entry.get('answers_list'))==0):
                return Response("Bad entry! Please make sure to add some answers to your poll..",status=400, mimetype="application/json")
            
                
            #create in database
            
            result = poll_col.insert_one(new_entry)
            
            id = result.inserted_id
            
            response_text =   str({"pol_id":id})  
            return Response(response_text,status=201, mimetype='application/json')
            
        except:

            return Response("Bad entry! Please make sure that the entry match the especification in the documentation",status=400, mimetype="application/json")






class Poll (Resource):
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
                return Response("Bad entry! Please make sure to enter a valid answer",status=404,mimetype="application/json")

        except: 
            return Response("Bad entry! Please make sure to enter a valid poll id",status=404,mimetype="application/json")



        return #brings the whole poll and it's results
    def post(self):

        return

api.add_resource(Poll,"/api/poll/<string:id>")

api.add_resource(Polls,"/api/polls/")








if __name__ == "__main__":
    app.run(debug=True)



