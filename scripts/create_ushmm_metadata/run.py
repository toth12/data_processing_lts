from get_camp_names import getCampNames
from get_ghetto_names import getGhettoNames
from get_gender import getGender
from get_interview_summary import getInterviewSummary
from get_interview_year import getInterviewYear
from get_interviewee_name import getIntervieweeName
from get_interview_title import getInterviewTitle
from get_shelfmark import getShelfmark
from get_provenance import getProvenance
import get_videos as mediaExtraction
import constants

import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
import csv
import pprint

pp = pprint.PrettyPrinter(indent=4)

# database info
DB = constants.DB
INPUT_COLLECTION = constants.INPUT_COLLECTION
OUTPUT_COLLECTION = constants.OUTPUT_COLLECTION
ORIGINAL_DATABASE = "USHM"
"""
def retrieveMissingFields(id_, row):
    missing_fields = row[1]

    for field in missing_fields:
        if field == "interviewee_name":
"""     

def populateDocument(document, unknown_fields, dictionary, id_, field_name):
    """
    If a specific field exists for a given interview (id_), 
    add the field the mongo document. Else add to the field
    of unkown_fields
    """
    if dictionary.get(id_, None) != None:
        document[field_name] = dictionary[id_]
    elif field_name != 'camp_names' and field_name != 'ghetto_names' and field_name != "interview_summary":
        # if no info, store it as a null value and add it to missing field
        document[field_name] = None
        unknown_fields.append(field_name)
    else:
        document[field_name] = ''
                
if __name__ == "__main__":
    """
    Queries the database to retrieve the interview_ids
    Populate document with the non-null data for each interview and insert
    created document to a new collection under 'Hol', name 'USHMM' database
    Generate a CSV spreadsheet with the missing field for each interview
    """
    # query for interview ids
    result = h.query(DB, INPUT_COLLECTION, {}, {'id':1} )
    interview_ids = [id_['id'] for id_ in result]

    # initialize dictionaries with all the pieces of information
    interviews_camp_names = getCampNames()
    interviews_ghetto_names = getGhettoNames()
    #interviewees_gender = getGender()
    interviews_year = getInterviewYear()
    interviews_summary = getInterviewSummary()
    interviewees_names = getIntervieweeName()
    interviews_titles = getInterviewTitle()
    interviews_shelfmarks = getShelfmark()
    interviews_provenances = getProvenance()
    interviews_htmls = mediaExtraction.getHTMLs()

    # initialize csv to record missing fields
    ofile  = open('output/USHM_missing_records.csv', "w")
    spreadsheet = csv.writer(ofile, quotechar='"', quoting=csv.QUOTE_ALL)

    # insert header
    header = [['interview_id', 'missing_fields', 'website_url', 'recording_year', 'gender', 'interviewee_name']]
    spreadsheet.writerows(header)

    # initialize csv to record missing thumbnail for .mp4
    ofile2  = open('output/USHM_missing_thumbnai.csv', "w")
    media_spreadsheet = csv.writer(ofile2, quotechar='"', quoting=csv.QUOTE_ALL)

    # insert header
    media_header = [['interview_id', 'url']]
    media_spreadsheet.writerows(media_header)

   
    # go over each interview and populate a document to be insert into Mongo
    for id_ in interview_ids:
        # initialize variables
        document = dict()
        unknown_fields = []

        # get html for the given interview
        html = interviews_htmls[id_]

        # extract videos and images urls from html
        media, type_of_media = mediaExtraction.getVideos(html)
        
        # populate document with media
        document["media_url"] = media
        document["thumbnail_url"] = ''

        # else if .mp4 media was found, save video and look for thumbnail
        if type_of_media == mediaExtraction.MP4:
            
            # get thumbnail image
            images = mediaExtraction.getImages(html)
        
            # populate thumbnail field, if any
            # if no thumbnail, record it on spreadsheet of missing media
            if images:
                document["thumbnail_url"] = images
            else:
                url = mediaExtraction.getWebsite(id_)
                unknown_media = [id_, url]
                media_spreadsheet.writerows([unknown_media])

        # if no media was found
        elif type_of_media == mediaExtraction.NO_MEDIA:
            unknown_fields.append("media_url")
        
        # populate fields with basic info from the original database
        document['interview_id'] = id_
        document['collection'] = 'USHMM'

        # populate remaining fields
        populateDocument(document, unknown_fields, interviews_year, id_, 'recording_year')
        populateDocument(document, unknown_fields, interviews_camp_names, id_, 'camp_names')
        populateDocument(document, unknown_fields, interviews_ghetto_names, id_, 'ghetto_names')
        populateDocument(document, unknown_fields, interviews_summary, id_, 'interview_summary')
        #populateDocument(document, unknown_fields, interviewees_gender, id_, 'gender')
        populateDocument(document, unknown_fields, interviewees_names, id_, 'interviewee_name')
        populateDocument(document, unknown_fields, interviews_titles, id_, 'testimony_title')
        populateDocument(document, unknown_fields, interviews_shelfmarks, id_, 'shelfmark')
        populateDocument(document, unknown_fields, interviews_provenances, id_, 'provenance')
        
        # if there were any fields missing in the interview, record themissing interviews in csv
        if unknown_fields:
            url = mediaExtraction.getWebsite(id_)
            columns = [id_, unknown_fields, url]

            # create csv entry
            spreadsheet.writerows([columns])
        
        # insert in the collection
        h.insert(DB, OUTPUT_COLLECTION, document)
 
