from get_camp_names import getCampNames
from get_ghetto_names import getGhettoNames
from get_gender import getGender
from get_interview_summary import getInterviewSummary
from get_interview_year import getInterviewYear
from get_interviewee_name import getIntervieweeName
from get_interview_title import getInterviewTitle
from get_shelfmark import getShelfmark
from get_provenance import getProvenance
from get_videos import getVideos, getWebsite, getHTML, getImages

import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
import csv
import pprint
import pdb
import time
pp = pprint.PrettyPrinter(indent=4)

def populateDocument(document, unknown_fields, dictionary, id_, field_name):
    """
    If a specific field exists for a given interview (id_), 
    add the field the mongo document. Else add to the field
    of unkown_fields
    """
    if dictionary.get(id_, None) != None:
        document[field_name] = dictionary[id_]
    elif field_name != 'camp_names' and field_name != 'ghetto_names' and field_name != "interview_summary":
        unknown_fields.append(field_name)
                
if __name__ == "__main__":
    """
    Queries the database to retrieve the interview_ids
    Populate document with the non-null data for each interview and insert
    created document to a new collection under 'Hol', name 'USHMM' database
    Generate a CSV spreadsheet with the missing field for each interview
    """
    # query for ghettos
    result = h.query('let_them_speak_data_processing', 'input_ushmm_metadata', {}, {'id':1} )
    interview_ids = [(id_['id'],id_['_id']) for id_ in result]

   
    # go over each interview and populate a document to be insert into Mongo
    for element in interview_ids:
        id_=element[0]
        document = dict()
        unknown_fields = []
        time.sleep(2)
        # get website url and html
        url = getWebsite(id_)
        html = getHTML(url)

       
        document['collection'] = "USHM"
        
        h.update_entry('let_them_speak_data_processing', 'input_ushmm_metadata', element[1],{'website_html':html})
