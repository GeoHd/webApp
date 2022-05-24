
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

        return

    def post(self):
        try:
            dictionary = dict(request.get_json())
            print(dictionary)
            answers_list = {}
            for answer in  list(dictionary.get('answers_list')):
                answers_list[answer]=0
            new_entry = {'question':str(dictionary.get('question')),'answers_list':answers_list}
            
    
            
            if (len(new_entry.get('question'))==0):
                abort (400,message="It looks like there is no question in your poll..")
            elif (len(new_entry.get('answers_list'))==0):
                abort (400,message="It looks like your pol has no answers..")
            
                
            #create in database
            
            result = poll_col.insert_one(new_entry)
            print(1234)
            
            id = result.inserted_id
            
            response_text =   str({"pol_id":id})  
            return Response(response_text,status=201, mimetype='application/json')
            
        except:
            abort(400, message="Bad entry! Please make sure that the entry match the especification in the documentation")



#todos = db.todo #Select the collection



class Poll (Resource):
    def get(self,id):
        try:
            result = poll_col.find_one({"_id":id})
            return result

        except:
            abort(400, message="Bad entry! Please make sure to enter a valid poll id")
        
    def put(self,id):
        try:
            dictionary = dict(request.get_json())
            chosen_answer = list(dictionary.values())[0]
            poll_dict = str(poll_col.find_one(ObjectId(id)))
            poll_dict =ast.literal_eval(poll_dict.replace("ObjectId(","").replace(")",""))
            print(poll_dict)
            
            answers_list = poll_dict["answers_list"]
            if chosen_answer in answers_list:
                answers_list[chosen_answer]+=1
                print(answers_list)
                poll_dict["answers_list"]=answers_list
                poll_col.find_one_and_update(filter={"_id":ObjectId(id)},update={'$set':{"answers_list":answers_list}},return_document=ReturnDocument.AFTER)
                print(poll_dict)
                return Response(str(poll_dict),status=200,mimetype='application/json')
            else:
                abort(400, message="Bad entry! Please make sure to enter a valid answer")

        except: 
            abort(400, message="Bad entry! Please make sure to enter a valid poll id")



    def post(self):
        return
    
class Hotel (Resource):
    def get(self,id):
        if (id == None):
            
            return # get all the open polls
        



        return #brings the whole poll and it's results
    def post(self):

        return

api.add_resource(Poll,"/api/poll/<string:id>")

api.add_resource(Polls,"/api/polls/")

api.add_resource(Hotel,"/api/hotels/<string:name>")







if __name__ == "__main__":
    app.run(debug=True)



