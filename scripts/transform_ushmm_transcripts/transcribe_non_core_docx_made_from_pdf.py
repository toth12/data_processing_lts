import sys, glob, os
#import helper_mongo as h
from docx import Document
from subprocess import call

import pprint
import constants
import re
import pdb

TRACKER = constants.USHMM_TRACKER_COLLECTION
OUTPUT = constants.OUTPUT_COLLECTION_USHMM
DB = constants.DB
INPUT_FOLDER=constants.INPUT_FOLDER_USHMM_TRANSCRIPTS_PDF_TRANSFORMED_TO_DOCS


def getUnstructured50_583Units(filename):
    """
    Returns the unstructured units of the RG-50.583 series
    These interviews did not Question and Answer to distinguish units but uses the distinction of bold and italic
    """
    doc = Document(filename)
    units = list()

    
    

    # iterate over all paragraphs to get text units
    for para in doc.paragraphs:
        paragraph = para.text
        
        # ensure paragraph is not just empty line
        hasText = paragraph.lstrip()
        # ensure it is not an empty line
        if hasText:


            # marks the end of the interview
            if "shttp://collections.ushmm.org/search/catalog/irn43329" in paragraph.lower() in paragraph.lower() :
                break
            else:
                units.append({'unit':paragraph})
    return units


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

    return units

def createStructuredTranscriptDoc():
    """
    Processes the 509 doc files beloging to the core asset in data
    Core asset is identified by numbers RG-50.030, RG-50.106, RG-50.549
    """
    

    core_doc_asset = []

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
    for file in core_doc_asset:
        # get text units for this entry

        if ("RG-50.583" in file):
            getUnstructured50_583Units(file)
        else:
            units = getTextUnits(file)

        if units:
            # get RG number
            original_filename = file.split('/')[-1]
            rg_number=original_filename.split("_")[0]

            # find last occurrence of '.' and replace it with '*' 
            k = rg_number.rfind(".")
            mongo_rg = rg_number[:k] + "*" + rg_number[k+1:]

            # insert units on the output collection
            #h.update_field(DB, OUTPUT, "shelfmark", mongo_rg, "structured_transcript", units)

            
            # update status on the stracker
            
            #h.update_field(DB, TRACKER, "microsoft_doc_file", original_filename, "status", "Processed")
        

        else:
            #update field to not processed here, log it
            print 'problem'
            

    

    pdb.set_trace()
    # success
    pprint.pprint("Core_doc_asset was successfully processed.")

if __name__ == "__main__":
    createStructuredTranscriptDoc()

   

    #getTextUnits()
    """
    result = h.query(DB, OUTPUT, { "structured_transcript": {'$exists': 'true'}}, {'id': 0})
    pprint.pprint(result)
    """
