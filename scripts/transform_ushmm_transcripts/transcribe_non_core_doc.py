import sys, glob, os
import helper_mongo as h
from data_spec import create_dictionary_of_file_list
import pdb
from get_text_units import getTextUnits


from docx import Document
from subprocess import call

import pprint
import constants
import re
from collections import defaultdict

TRACKER = constants.USHMM_TRACKER_COLLECTION
OUTPUT = constants.OUTPUT_COLLECTION_USHMM
DB = constants.DB
INPUT_FOLDER=constants.INPUT_FOLDER_USHMM_TRANSCRIPTS_DOC
OUTPUT_FOLDER_USHMM_PROCESSING_LOGS=constants.OUTPUT_FOLDER_USHMM_PROCESSING_LOGS 

pp = pprint.PrettyPrinter(indent=4)

def safePrint(str_):
    return ''.join(i for i in str_ if ord(i) < 128)



def createStructuredTranscript_Non_Core_Doc(debug=False):
    """
    Processes the 509 doc files beloging to the core asset in data
    Core asset is identified by numbers RG-50.030, RG-50.106, RG-50.549
    """

    #create a temporary folder that will hold the data transformed from doc to docx
    os.system('mkdir ' + INPUT_FOLDER+'temp')

    core_doc_asset = []
    missing_count = 0
    missing_files=[]
    # get all the docx files that are part of the core asset
    for file in glob.glob(INPUT_FOLDER+"*.doc"):

        # RG numbers for the core asset
        if ("RG-50.030" not in file and
            "RG-50.106" not in file and
            "RG-50.549" not in file):
        

           
            # convert file to docx, storing it in an untracked folder called temp
            file_docx = file + 'x'
            command = 'textutil -convert docx ' + file + ' -output ' + INPUT_FOLDER+'temp/'+ file_docx.split('/')[-1]
            call(command, shell=True)

            # append to the array
            core_doc_asset.append(file_docx)
    

     

    # get the units for each file, store them and update tracker
    core_doc_asset=create_dictionary_of_file_list(core_doc_asset)
   
    not_processed=0
    processed_doc=0
    
    # get the units for each file, store them and update tracker 
    for c, mongo_rg in enumerate(core_doc_asset):
        #set the debugger
    
        if (debug == True) and (c==3):
            break
        # get text units for this entry
        processed=[]
        result=[]
        
        for file in core_doc_asset[mongo_rg]:
            
            
            
            units = getTextUnits(INPUT_FOLDER+'temp/'+file.split('/')[-1])
            
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
        h.update_field(DB, TRACKER, "rg_number", mongo_rg, "method", "transcribe_non_core_doc")

        not_processed=not_processed+1

        if False in processed:

            h.update_field(DB, TRACKER, "rg_number", mongo_rg, "status", "Unprocessed")
            not_processed=not_processed+1
            missing_files.append(' '.join(core_doc_asset[mongo_rg]))
        else:
            # insert units on the output collection
            h.update_field(DB, OUTPUT, "shelfmark", 'USHMM '+mongo_rg, "structured_transcript", result)

                
            # update status on the stracker
                
            h.update_field(DB, TRACKER, "rg_number", mongo_rg, "status", "Processed")
            processed_doc=processed_doc+1
           

    #delete the temporary folder
    os.system('rm -r ' + INPUT_FOLDER+'temp')

   
    #write the missing files to text file
    file = open(OUTPUT_FOLDER_USHMM_PROCESSING_LOGS+'transcribe_non_core_doc_failed.txt','w')
    file.write('\n'.join(missing_files))

    
    # success
    pprint.pprint("Non-core doc files were successfully processed, but there are " +  str(missing_count) + " missing")

if __name__ == "__main__":
    createStructuredTranscript_Non_Core_Doc()
    #TODO account for the fact that ongoing answers in different paragaphs can exist
   