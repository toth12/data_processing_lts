import sys, glob, os
import helper_mongo as h
from docx import Document
from subprocess import call
from data_spec import create_dictionary_of_file_list

import pprint
import constants
import re
import pdb

TRACKER = constants.USHMM_TRACKER_COLLECTION
OUTPUT = constants.OUTPUT_COLLECTION_USHMM
DB = constants.DB
INPUT_FOLDER=constants.INPUT_FOLDER_USHMM_TRANSCRIPTS_PDF_TRANSFORMED_TO_DOCS
OUTPUT_FOLDER_USHMM_PROCESSING_LOGS=constants.OUTPUT_FOLDER_USHMM_PROCESSING_LOGS 

def getTextUnits(filename):
    doc = Document(filename)
    units = list()
    # iterate over all paragraphs to get text units
    
    for para in doc.paragraphs:
        paragraph = para.text
        
        
        # ensure it is not an empty line
        if paragraph:
            # get first word
            unit_type = paragraph.partition(' ')[0]
            
            # e.g [d]
            m = re.compile('[A-Z][.|:]')
            type1 = m.match(unit_type)

            # e.g [WJ]
            n = re.compile('\[[A-Z][A-Z]\]')
            typer2= n.match(unit_type)

            # else parse them according to formatting guidelines
            if ("Question:" in unit_type or
                type1 or
                "Answer:" in unit_type or 
                typer2):

                units.append({'unit': paragraph})
            
            # backup for 2 interviews that don't match any of the patterns above
            elif (filename == "RG-50.030.0336_trs_en.docx" or 
                filename == "RG-50.030.0335_trs_en.docx"):

                if ("Interviewer:" in unit_type or 
                    "Theodore:" in unit_type or 
                    "MR." in unit_type):
                    
                    units.append({'unit': paragraph})
            else:
                if len(units)>0:
                    units[-1]['unit']= units[-1]['unit']+paragraph       
    print units
    
    return units






def createStructuredTranscriptDoc():
    """
    Processes the 509 doc files beloging to the core asset in data
    Core asset is identified by numbers RG-50.030, RG-50.106, RG-50.549
    """
    

    core_doc_asset = []
    missing_files=[]

    # get all the docx files that are part of the core asset
    for file in glob.glob(INPUT_FOLDER+"*.docx"):
        # RG numbers for the core asset
        if ("RG-50.030" in file or
            #this is questionable
            "RG-50.106" in file or
            "RG-50.549" in file):

            
            
            # append to the array
            core_doc_asset.append(file)

    

    # get the units for each file, store them and update tracker
    not_processed=0
    processed_doc=0



    core_doc_asset=create_dictionary_of_file_list(core_doc_asset)
    
    for mongo_rg in core_doc_asset:
        # get text units for this entry
        processed=[]
        result=[]
        
        for file in core_doc_asset[mongo_rg]:

            if ("RG-50.583" in file):
                units=getUnstructured50_583Units(file)
            else:
                units = getTextUnits(file)
            
            if units:
                result.extend(units)
            
                processed.append(True)
            else:
                #check if processed
                processed.append(False)

        #set the method used to transform the transcript
            
        h.update_field(DB, TRACKER, "rg_number", mongo_rg, "method", "transcribe_core_docx_made_from_pdf")

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

    
    #write the missing files to text file
    file = open(OUTPUT_FOLDER_USHMM_PROCESSING_LOGS+'transcribe_core_docx_made_from_pdf_failed.txt','w')
    file.write('\n'.join(missing_files))
    
    # success
    pprint.pprint("Core_docx_asset_made_from_pdf was successfully processed.")
    

if __name__ == "__main__":
    createStructuredTranscriptDoc()

   

    #getTextUnits()
    """
    result = h.query(DB, OUTPUT, { "structured_transcript": {'$exists': 'true'}}, {'id': 0})
    pprint.pprint(result)
    """
