from pymongo import MongoClient
import pdb
import ast
from bson.objectid import ObjectId

def query(db_name,collection_name,query,projection): 
	"""Takes a db name, collection name, query and projection as input, and returns the result as a list"""
	client = MongoClient()
	client = MongoClient('localhost', 27017)
	db = client[db_name]
	collection = db[collection_name]
	#        pdb.set_trace()
	result = []
	for results in collection.find(query,projection):
		result.append(results)
	client.close()	
	return result


def findDocs(db_name,collection_name): 
	"""Takes a db name, collection name, query and projection as input, and returns the result as a list"""
	client = MongoClient()
	client = MongoClient('localhost', 27017)
	db = client[db_name]
	collection = db[collection_name]
	#        pdb.set_trace()
	result = []
	for results in collection.find():
		result.append(results)
	client.close()	
	return result

def update_entry(db_name,collection_name,entry_id,new_field):
	client = MongoClient()
	client = MongoClient('localhost', 27017)
	db = client[db_name]
	collection = db[collection_name]


	collection.update({'_id' : entry_id}, {'$set':new_field})
	client.close()


def delete_field(db_name,collection_name,field_to_delete):
	"""Takes a db name, collection name, and a field to be deleted and removes that field"""
	client = MongoClient()
	client = MongoClient('localhost', 27017)
	db = client[db_name]
	collection = db[collection_name]

	# multi=True deletes this field from all documents, otherwise only the field in  the first retrieved entry is deleted
	r=collection.update({}, {'$unset': {field_to_delete:1}}, multi=True)

	#result of the updating operation can be accessed by printing r
	client.close()




def aggregate(db_name,collection_name,pipeline):
	"""Takes a DB name, collection name, a pipeline (a list), and carries out an aggregation"""

	client = MongoClient()
	client = MongoClient('localhost', 27017)
	db = client[db_name]


	collection = db[collection_name]

	result = collection.aggregate(pipeline)
	client.close()

	return result

def delete(db_name,collection_name,criteria):
	"""Takes a DB name, collection name, a criteria (a python dictionary, for instance: {'_id':result[0]['_id']}), and carries out the deletion of the corresponding entries. The function uses the delete_many function """

	client = MongoClient()
	client = MongoClient('localhost', 27017)
	db = client[db_name]
	collection = db[collection_name]

	result=collection.delete_many(criteria)

	# the number of deleted entries can obtained with result.deleted_count
	client.close()

	return result


def insert(db_name,collection_name,data):
	"""Takes a DB name, collection name, a data (a python dictionary), and inserts it into the collection, this uses insertone method """

	client = MongoClient()
	client = MongoClient('localhost', 27017)
	db = client[db_name]
	collection = db[collection_name]

	result = collection.insert(data,check_keys=False)

	# the unique id of the inserted entry can be obtained with result.inserted_id
	client.close()

	return result


if __name__ == "__main__":
	#query example

	#result= query('Hol','USHM',{'language':'English' },{'_id':1})


	#update example

	#update_entry('Hol','articles',1,{'lnguage':'suah'})

	#aggregate example

	#pipeline= [{'$match': { '$and': [ {'language':{'$size':1}},{'language':"English"}]}},{ '$out' : "undress_experiment_test" }]

	#aggregate('Hol','USHM',pipeline)

	#delete example

	#result = delete("Hol",'undress_experiment_test',{"_id": ObjectId('583e0a86ad16910447c8da37')})
	# print result.deleted_count	

	#delete example

	#	delete_field('Hol','undress_experiment_2','sentence_chunked_lemmatized')
	print('main')
