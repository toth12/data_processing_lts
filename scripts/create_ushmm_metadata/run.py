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
    result = h.query('Hol', 'undress_experiment', {}, {'id':1} )
    interview_ids = [id_['id'] for id_ in result]

    # initialize dictionaries with all the pieces of information
    interviews_camp_names = getCampNames()
    interviews_ghetto_names = getGhettoNames()
    interviewees_gender = getGender()
    interviews_year = getInterviewYear()
    interviews_summary = getInterviewSummary()
    interviewees_names = getIntervieweeName()
    interviews_titles = getInterviewTitle()
    interviews_shelfmarks = getShelfmark()
    interviews_provenances = getProvenance()

    # initialize csv to record missing fields
    ofile  = open('USHM_missing_records.csv', "w")
    spreadsheet = csv.writer(ofile, quotechar='"', quoting=csv.QUOTE_ALL)

    # insert header
    header = [['interview_id', 'missing_fields', 'website_url', 'recording_year', 'gender', 'interviewee_name']]
    spreadsheet.writerows(header)

    # go over each interview and populate a document to be insert into Mongo
    for id_ in interview_ids:
        document = dict()
        unknown_fields = []

        # get website url and html
        url = getWebsite(id_)
        html = getHTML(url)

        # extract videos and images urls from  
        videos = getVideos(html)
        images = getImages(html)
        
        # populate thumbnail pictures
        if images:
            document["media_thumbnail"] = images
        else:
            unknown_fields.append("media_thumbnail")

        # populate videos, if any
        if videos:
            document["media_url"] = videos
        else:
            unknown_fields.append("media_url")

        # populate fields
        document['ushhm_unique_id'] = id_
        document['original_html'] = html

        # populate remaining fields
        populateDocument(document, unknown_fields, interviews_year, id_, 'recording_year')
        populateDocument(document, unknown_fields, interviews_camp_names, id_, 'camp_names')
        populateDocument(document, unknown_fields, interviews_ghetto_names, id_, 'ghetto_names')
        populateDocument(document, unknown_fields, interviews_summary, id_, 'interview_summary')
        populateDocument(document, unknown_fields, interviewees_gender, id_, 'gender')
        populateDocument(document, unknown_fields, interviewees_names, id_, 'interviewee_name')
        populateDocument(document, unknown_fields, interviews_titles, id_, 'testimony_title')
        populateDocument(document, unknown_fields, interviews_shelfmarks, id_, 'shelfmark')
        populateDocument(document, unknown_fields, interviews_provenances, id_, 'historical_provenance')
        
        # if there were any fields missing in the interview, record themissing interviews in csv
        if unknown_fields:
            url = getWebsite(id_)
            columns = [id_, unknown_fields, url]

            # create csv entry
            spreadsheet.writerows([columns])

        document['collection'] = "USHM"
        
        h.insert('Hol', 'USHMM', document)