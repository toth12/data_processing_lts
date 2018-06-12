from pymongo import MongoClient
import pprint
import sys, glob, os
import constants
import pdb
#helper_path = os.path.join("..", "..", "utils")
#sys.path.insert(0, helper_path)



import helper_mongo as h






# initial status for all files in the tracker
INITIAL_STATUS = "not processed"
DB = constants.DB
INPUT_COLLECTION = constants.INPUT_COLLECTION_USHMM
TRACKER = constants.USHMM_TRACKER_COLLECTION
INPUT_FOLDER=constants.INPUT_FOLDER_USHMM_TRANSCRIPTS_DOC

def getDocs():
    """
    Returns a dictionary with all the docs available in the 
    data folder. Maps the rg_number from the database to the 
    file name
    """
    docs = dict()
    for file in glob.glob(INPUT_FOLDER+"*"):
        # get RG number
        rg_number = file.split('/')[-1].split("_")[0]

        # find last occurrence of '.' and replace it with '*' 
        k = rg_number.rfind(".")
        mongo_rg = rg_number[:k] + "*" + rg_number[k+1:]

        # add it to dictionary
        docs[mongo_rg] = file.split('/')[-1]
        
    # return
    return docs

def createTracker():
    """
    Goes over all the transcripts in the data folder and creates a tracker
    for all the interviews
    """
    # query for interview ids
    result = h.query(DB, INPUT_COLLECTION, {}, {'id':1, 'rg_number': 1, 'fnd_doc_filename': 1} )
    
    docs = getDocs()
    for interview in result:
        # instantiate document to be inserted and get rg_number
        document = dict()
        rg_number = interview['rg_number']

        # populate document
        document['id'] = interview['id']
        document['rg_number'] = rg_number

        #filter pdfs files and only those that are in fact transcripts
        document['pdf_transcripts'] = [element for element in interview['fnd_doc_filename'] if 'trs' in element ]
        
        document['microsoft_doc_file'] = docs.get(rg_number, "")
        document['status'] = INITIAL_STATUS
        
         # insert document in tracker
        h.insert(DB, TRACKER, document)

    # success message
    pprint.pprint("Tracker successfully created!")

if __name__ == "__main__":
    createTracker()
