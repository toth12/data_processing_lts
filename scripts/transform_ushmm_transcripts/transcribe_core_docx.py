import sys, glob, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
from data_spec import create_dictionary_of_file_list
import pdb
from get_text_units import getTextUnits


from docx import Document
import pprint
import constants

TRACKER = constants.USHMM_TRACKER_COLLECTION
OUTPUT = constants.OUTPUT_COLLECTION_USHMM
DB = constants.DB
INPUT_FOLDER=constants.INPUT_FOLDER_USHMM_TRANSCRIPTS_DOC
OUTPUT_FOLDER_USHMM_PROCESSING_LOGS=constants.OUTPUT_FOLDER_USHMM_PROCESSING_LOGS 




def createStructuredTranscriptDocx(debug=False):
    """
    Processes the 82 docx files beloging to the core asset in data
    Core asset is identified by numbers RG-50.030, RG-50.106, RG-50.549
    """
    core_docx_asset = []

    # get all the docx files that are part of the core asset
    for file in glob.glob(INPUT_FOLDER+"*.docx"):

        # RG numbers for the core asset
        if ("RG-50.030" in file or
            "RG-50.106" in file or
            "RG-50.549" in file):
        #this is temporary

            # append to the array
            core_docx_asset.append(file)

    core_doc_asset=create_dictionary_of_file_list(core_docx_asset)
   
    missing_count = 0
    missing_files=[]
    not_processed=0
    processed_doc=0#copy here
    for c, mongo_rg in enumerate(core_doc_asset):
        #set the debugger
        if (debug == True) and (c==3):
            break
        # get text units for this entry
        processed=[]
        result=[]
        
        for file in core_doc_asset[mongo_rg]:

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
        h.update_field(DB, TRACKER, "rg_number", mongo_rg, "method", "transcript_core_docx")

        

        if False in processed:
            h.update_field(DB, TRACKER, "rg_number", mongo_rg, "status", "Unprocessed")

            #set the method used to transform the transcript

            h.update_field(DB, TRACKER, "rg_number", mongo_rg, "method", "transcribe_core_docx")

            not_processed=not_processed+1
            missing_files.append(' '.join(core_doc_asset[mongo_rg]))
        else:
            # insert units on the output collection
            h.update_field(DB, OUTPUT, "shelfmark",'USHMM '+mongo_rg, "structured_transcript", result)

                
            # update status on the stracker
                
            h.update_field(DB, TRACKER, "rg_number", mongo_rg, "status", "Processed")
            processed_doc=processed_doc+1


     #write the missing files to text file
    file = open(OUTPUT_FOLDER_USHMM_PROCESSING_LOGS+'transcribe_core_docx_failed.txt','w')
    file.write('\n'.join(missing_files))
    pprint.pprint("Core_docx_asset was successfully processed.")

if __name__ == "__main__":
    createStructuredTranscriptDocx()
    """
    result = h.query(DB, OUTPUT, { "structured_transcript": {'$exists': 'true'}}, {'id': 0})
    pprint.pprint(result)
    """
