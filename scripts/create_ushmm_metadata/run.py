from get_camp_names import getCampNames
from get_ghetto_names import getGhettoNames
from get_gender import getGender
from get_interview_summary import getInterviewSummary
from get_interview_year import getInterviewYear
from get_interviewee_name import getIntervieweeName
from get_interview_title import getInterviewTitle
from pymongo import MongoClient
import concurrent.futures
import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h

import pprint
pp = pprint.PrettyPrinter(indent=4)


# create the collection
client = MongoClient()
db = client['Hol']
collection = db['USHMM']

# initialize dictionaries with all the pieces of information
interview_ids, interviews_camp_names = getCampNames()
interviews_ghetto_names = getGhettoNames()
interviewees_gender = getGender()
interviews_year = getInterviewYear()
interviews_summary = getInterviewSummary()
intervewees_names = getIntervieweeName()
interviews_titles = getInterviewTitle()

# go over each interview and get appropriate fields
for id_ in interview_ids:
    document = dict()

    # populate fields
    document['ushhm_unique_id'] = id_
    document['recording_year'] = interviews_year.get(id_, None)
    document['camp_names'] = interviews_camp_names.get(id_, None)
    document['ghetto_names'] = interviews_ghetto_names.get(id_, None)
    document['interview_summary'] = interviews_summary.get(id_, None)
    document['gender'] = interviewees_gender.get(id_, None)
    document['interviewee_name'] = intervewees_names.get(id_, None)
    document['testimony_title'] = interviews_titles.get(id_, None)
    
    db.collection.insert(document)

client.close()
    

    
    

