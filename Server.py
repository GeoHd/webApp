#from flask import Flask # For flask implementation
#from flask_restful import Api, Resource
from pymongo import MongoClient # Database connector


'''
mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)    #Configure the connection to the database
db = client.cisco    #Select the database
'''

#todos = db.todo #Select the collection



app = Flask(__name__)
api = Api(app)







if __name__ == "__main__":
    app.run(debug=True)



