import sys, glob, os
import helper_mongo as h
from data_spec import create_dictionary_of_file_list
import pdb
from get_text_units import getTextUnits



from docx import Document
from collections import defaultdict
from subprocess import call

import pprint
import constants
import re

TRACKER = constants.USHMM_TRACKER_COLLECTION
OUTPUT = constants.OUTPUT_COLLECTION_USHMM
DB = constants.DB
INPUT_FOLDER=constants.INPUT_FOLDER_USHMM_TRANSCRIPTS_DOC
OUTPUT_FOLDER_USHMM_PROCESSING_LOGS=constants.OUTPUT_FOLDER_USHMM_PROCESSING_LOGS 

def safePrint(str_):
    """
    Strips all the non-ascii characters
    """
    return ''.join(i for i in str_ if ord(i) < 128)

 
def createStructuredTranscript_Non_Core_Docx():
    """
    Creates the structure dunits for the for the 132 files
    that are part of the non-core asset and which have the
    docx extension
 
    Missing interviews are piped into the file entitled missing_non_core file
    """
    docx_assets = []
    missing_count = 0
    missing_files=[]
    for file in glob.glob(INPUT_FOLDER+"*.docx"):
         # RG numbers for the non-core asset
        if ("RG-50.030" not in file and
            "RG-50.106" not in file and
            "RG-50.549" not in file):
            docx_assets.append(file)
        


    # get the units for each file, store them and update tracker
    not_processed=0
    processed_doc=0



    core_doc_asset=create_dictionary_of_file_list(docx_assets)
    
    for mongo_rg in core_doc_asset:
        # get text units for this entry
        processed=[]
        result=[]
        
        for file in core_doc_asset[mongo_rg]:

            #add file specific methods here

            
            units = getTextUnits(file)
            
            if units:

                #replace white spaces
                for i,element in enumerate(units):
                    units[i]['unit']=' '.join(element['unit'].split())
                
                result.extend(units)

                
            
                processed.append(True)
            else:
                #check if processed
                processed.append(False)
        #set the method used to transform the transcript
        

        h.update_field(DB, TRACKER, "rg_number", mongo_rg, "method", "transcribe_non_core_docx")

        not_processed=not_processed+1
        if False in processed:
            h.update_field(DB, TRACKER, "rg_number", mongo_rg, "status", "Unprocessed")
            missing_files.append(' '.join(core_doc_asset[mongo_rg]))
            not_processed=not_processed+1
        else:
            # insert units on the output collection
            h.update_field(DB, OUTPUT, "shelfmark", 'USHMM '+mongo_rg, "structured_transcript", result)
            
                
            # update status on the stracker
            
            h.update_field(DB, TRACKER, "rg_number", mongo_rg, "status", "Processed")
            processed_doc=processed_doc+1    
    
    print "The files above could not be processed; they are logged in: "+OUTPUT_FOLDER_USHMM_PROCESSING_LOGS 
   
    #write the missing files to text file
    file = open(OUTPUT_FOLDER_USHMM_PROCESSING_LOGS+'transcribe_non_core_docx_failed.txt','w')
    file.write('\n'.join(missing_files))

    print missing_count



    # success
    pprint.pprint("Non-core doc files were successfully processed, but there are " +  str(missing_count) + " missing")
    

if __name__ == "__main__":
    createStructuredTranscript_Non_Core_Docx()
    #TODO handle the 005 exception