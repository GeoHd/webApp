
from flask import Flask, request, jsonify # For flask implementation
from flask_restful import Api, Resource, abort
import pymongo
from pymongo import MongoClient # Database connector
import os



mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)    #Configure the connection to the database
db = client.cisco    #Select the database



app = Flask(__name__)
api = Api(app)


class Polls (Resource):
    def get(self):
        
        return

    def post(self):
        try:
            dictionary = dict(request.get_json())
            print(dictionary)
            new_entry = {'question':str(dictionary.get('question')),'answers_list':list(dictionary.get('answers_list'))}
            
    
            
            if (len(new_entry.get('question'))==0):
                abort (400,message="It looks like there is no question in your poll..")
            elif (len(new_entry.get('answers_list'))==0):
                abort (400,message="It looks like your pol has no answers..")
            
                
            pol_id = 0
            #create in database
            collection = db["Polls"]
            collection.insert_one(new_entry)
            
            
            return pol_id
            
        except:
            
            abort(400, message="Bad entry! Please make sure that the entry match the especification in the documentation")



#todos = db.todo #Select the collection



class Poll (Resource):
    def get(self,id):
        print(request.form)

        if (type(id)==int):
            try:
                return
            except:
                abort(404,"There is no poll with the given id number")
    
        else:
            abort(404,message="Bad entry. Please make sure to enter a valid poll id number")
        
    


    def post(self):
        return
    
class Hotel (Resource):
    def get(self,id):
        if (id == None):
            
            return # get all the open polls
        



        return #brings the whole poll and it's results
    def post(self):

        return

api.add_resource(Poll,"/api/poll/<int:id>")

api.add_resource(Polls,"/api/polls/")

api.add_resource(Hotel,"/api/hotels/<string:name>")







if __name__ == "__main__":
    app.run(debug=True)



