# -*- coding: utf-8 -*-
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
from text import transform_fields_with_non_latin_characters_to_latin
import sys, os
import pandas as pd
import pdb
import helper_mongo as h
import csv
import pprint

import re

pp = pprint.PrettyPrinter(indent=4)

# database info
DB = constants.DB
INPUT_COLLECTION = constants.INPUT_COLLECTION_USHMM
OUTPUT_COLLECTION = constants.OUTPUT_COLLECTION_USHMM
ORIGINAL_DATABASE = "USHM"
MANUAL_INPUT_CSV = "USHM_missing_records_ELLIOT.csv"
INPUT_FOLDER=constants.INPUT_FOLDER_USHMM_METADATA
OUTPUT_FOLDER=constants.OUTPUT_FOLDER_USHMM_PROCESSING_LOGS
INPUT_DATA='input_ushmm_metadata.bson'

def retrieveMissingFields():
    backup = dict()

    with open(INPUT_FOLDER + MANUAL_INPUT_CSV, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)
        for row in spamreader:
            
            id_ = row[0]
            info = dict()

            # store gender if any
            if row[3] != "":
                info["interviewee_name"] = row[3]
            
            if row[4] != "":
                info["gender"] = row[4]

            if row[5] != "":
                info["recording_year"] = row[5]

            if row[6] != "":
                info["comments"] = row[6]
            else:
                info["comments"] = ""

            backup[id_] = info

    return backup        

def populateDocument(document, unknown_fields, dictionary, id_, field_name, manual_backup):
    """
    If a specific field exists for a given interview (id_), 
    add the field the mongo document. Else add to the field
    of unkown_fields
    """
    # populate data if possible
    if dictionary.get(id_, None) != None:
        document[field_name] = dictionary[id_]
    
    # check if csv manual backup has info needed
    elif manual_backup.get(id_, None) != None and field_name in manual_backup[id_]:
        info = manual_backup[id_]
        document[field_name] = info[field_name]

    ### even if no info was found, populate the entry with a null-equivalent value 
    elif field_name == 'camp_names' or field_name == 'ghetto_names':
        document[field_name]= []

    elif field_name == 'recording_year':
        document[field_name] = None

    # for all other missing fields, populate with empty string
    else:
        document[field_name] = ""

         # add it to missing field csv
        if field_name != 'interview_summary':
            unknown_fields.append(field_name)

def harmonize_camp_ghetto_names(field):
    names = h.query(DB, OUTPUT_COLLECTION, {}, {field: 1,'id':1} )

    #load the prepared data
    if field =="camp_names":

        df_variants = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'camp_variants_resolution_sheet.csv')
        df_to_remove = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'camp_names_remove_list.csv',header=None)
        df_to_correct = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'camp_names_correction_list.csv',encoding='utf-8')
    
    elif (field=="ghetto_names"):
        df_variants = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'ghetto_variants_resolution_sheet.csv')
        df_to_remove = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'ghetto_names_remove_list.csv',header=None)
        df_to_correct = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'ghetto_names_correction_list.csv',encoding='utf-8')
    


    try:
        for entry in names:
            print entry[field]
            if len(entry[field])==0:
                continue
            else:
                result=[]
                for name in entry[field]:
                    if name =='Block 10 (Auschwitz':
                        name = 'Auschwitz'

                    elif name in df_to_remove[0].to_list():
                        continue
                    elif not (df_to_correct[df_to_correct.original_form==name.encode('utf-8')].empty):
                        corrected_version = df_to_correct[df_to_correct.original_form==name.encode("utf-8")].final_form.values[0]
                        result.append(corrected_version)
                    elif not (df_variants[df_variants.variants.str.contains(name.encode('utf-8'))].empty):

                        variant_to_include = df_variants[df_variants.variants.str.contains(name.encode("utf-8"))].final_version.values[0]
                        result.append(variant_to_include)

                    else:
                        result.append(name.encode('utf-8'))
                
                h.update_field(DB,OUTPUT_COLLECTION, '_id', entry['_id'], field, result)
            
    except:
        pdb.set_trace()
    




                
def main():
    """
    Queries the database to retrieve the interview_ids
    Populate document with the non-null data for each interview and insert
    created document to a new collection under 'Hol', name 'USHMM' database
    Generate a CSV spreadsheet with the missing field for each interview
    """
    
    # takes the input collection (mongo collection exported to JSON) and imports it to the DB
    os.system('mongorestore -d ' + DB + ' -c '+INPUT_COLLECTION +' '+INPUT_FOLDER+INPUT_DATA)

    # query for interview ids
    result = h.query(DB, INPUT_COLLECTION, {}, {'id':1} )
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
    interviews_htmls = mediaExtraction.getHTMLs()

    # initialize csv to record missing fields
    ofile  = open(OUTPUT_FOLDER+'USHM_missing_records.csv', "w")
    spreadsheet = csv.writer(ofile, quotechar='"', quoting=csv.QUOTE_ALL)

    # insert header
    header = [['interview_id', 'missing_fields', 'website_url', 'interviewee_name', 'gender', 'recording_year']]
    spreadsheet.writerows(header)

    # initialize csv to record missing thumbnail for .mp4
    ofile2  = open(OUTPUT_FOLDER+'USHM_missing_thumbnai.csv', "w")
    media_spreadsheet = csv.writer(ofile2, quotechar='"', quoting=csv.QUOTE_ALL)

    # insert header
    media_header = [['interview_id', 'url']]
    media_spreadsheet.writerows(media_header)

    # get information from manual input csv with missing fields
    manual_backup = retrieveMissingFields()

    # go over each interview and populate a document to be insert into Mongo
    for id_ in interview_ids:
        # initialize variables
        #if id_=='irn508927':
            #pdb.set_trace()
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
        document['testimony_id'] = id_
        document['collection'] = 'USHMM'

        # if interview has multiple interviewees, leave it as an empty string, else populate
        if id_ in manual_backup:
            backup_info = manual_backup[id_]
            comment = backup_info["comments"]
            #change the interview year to integer
            if ('recording_year' in backup_info.keys()):
                backup_info["recoding_year"]=int(backup_info["recording_year"])
                
            if "Multiple interviewees" in comment:
                document["interviewee_name"] = ""
                document["gender"] = ""
            
            else:
                populateDocument(document, unknown_fields, interviewees_names, id_, 'interviewee_name', manual_backup)
                populateDocument(document, unknown_fields, interviewees_gender, id_, 'gender', manual_backup)
        else:
            populateDocument(document, unknown_fields, interviewees_names, id_, 'interviewee_name', manual_backup)
            populateDocument(document, unknown_fields, interviewees_gender, id_, 'gender', manual_backup)
        
        # populate remaining fields
        populateDocument(document, unknown_fields, interviews_year, id_, 'recording_year', manual_backup)
        populateDocument(document, unknown_fields, interviews_camp_names, id_, 'camp_names', manual_backup)
        populateDocument(document, unknown_fields, interviews_ghetto_names, id_, 'ghetto_names', manual_backup)
        populateDocument(document, unknown_fields, interviews_summary, id_, 'interview_summary', manual_backup)
        populateDocument(document, unknown_fields, interviews_titles, id_, 'testimony_title', manual_backup)
        populateDocument(document, unknown_fields, interviews_shelfmarks, id_, 'shelfmark', manual_backup)
        populateDocument(document, unknown_fields, interviews_provenances, id_, 'provenance', manual_backup)
        
        # if there were any fields missing in the interview, record themissing interviews in csv
        if unknown_fields:
            url = mediaExtraction.getWebsite(id_)
            columns = [id_, unknown_fields, url]

            # create csv entry
            spreadsheet.writerows([columns])
        
        # insert in the collection

        #make sure that interview year is an integer

        if (not isinstance(document['recording_year'],int)) and (document['recording_year'] is not None):
            document['recording_year']=int(document['recording_year'])
        #document=transform_fields_with_non_latin_characters_to_latin([document])
        
        h.insert(DB, OUTPUT_COLLECTION, document)
    #start the metadata harmonization
    harmonize_camp_ghetto_names(field='camp_names')
    harmonize_camp_ghetto_names(field='ghetto_names')
if __name__ == '__main__':
    harmonize_camp_ghetto_names(field='ghetto_names')

 