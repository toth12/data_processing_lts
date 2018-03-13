from pymongo import MongoClient
import pprint
import sys, glob, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h

# change directory to retrieve docs
os.chdir("../../data/")

# initial status for all files in the tracker
INITIAL_STATUS = "not processed"

def getIRNs():
    """
    Returns a dictionary with the irns of 1281 entries in
    the undress_experiment database
    """
    # query for interview years
    result = h.query('Hol', 'undress_experiment',  {}, {'rg_number': 1, 'id': 1})
    
    # initialize dictionary
    interviews_id = dict()

    # go through all the interviews
    for interview in result:
        key = interview.get('rg_number')
        
        # access date object
        interviews_id[key] = interview.get('id')

    return interviews_id

def getPDFs():
    """
    Returns a dictionary with the pdf transcript filenames 
    of 1281 entries in the undress_experiment database
    """
    # query for transcripts pdfs
    result = h.query('Hol', 'undress_experiment',  {}, {'rg_number': 1, 'fnd_doc_filename': 1})
    
    # initialize dictionary
    pdfs = dict()

    # go through all the interviews
    for interview in result:
        key = interview.get('rg_number')
        
        # access transcript object
        pdfs[key] = interview.get('fnd_doc_filename')

    return pdfs

if __name__ == "__main__":
    """
    Goes over all the transcripts in the data folder and creates a tracker
    for those 1281 interviews
    """

    docs = []
    interviews_irns = getIRNs()
    transcripts_pdfs = getPDFs()

    for file in glob.glob("*"):
        document = dict()
        # get RG number
        rg_number = file.split("_")[0]

        # find last occurrence of '.' and replace it with '*' 
        k = rg_number.rfind(".")
        mongo_rg = rg_number[:k] + "*" + rg_number[k+1:]
        
        # query for the given rn
        irn = interviews_irns[mongo_rg]
        pdf = transcripts_pdfs[mongo_rg]

        # populate fields
        document["microsoft_doc_file"] = file
        document["rg_number"] = rg_number
        document["id"] = irn
        document["pdf_transcripts"] = pdf
        document["status"] = "not processed"

        # insert document in tracker
        h.insert('Hol', 'USHMM_transcript_processing_progress', document)
    
    print "Tracker successfully created!"