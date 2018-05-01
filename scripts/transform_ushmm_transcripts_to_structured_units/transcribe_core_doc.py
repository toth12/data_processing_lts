import sys, glob, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h

os.chdir("../../data/")
from docx import Document
from subprocess import call

import pprint
import constants
import re


TRACKER = constants.TRACKER_COLLECTION
OUTPUT = constants.OUTPUT_COLLECTION
DB = constants.DB

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

def createStructuredTranscriptDocx():
    """
    Processes the 509 doc files beloging to the core asset in data
    Core asset is identified by numbers RG-50.030, RG-50.106, RG-50.549
    """
    core_doc_asset = []

    # get all the docx files that are part of the core asset
    for file in glob.glob("*.doc"):

        # RG numbers for the core asset
        if ("RG-50.030" in file or
            "RG-50.106" in file or
            "RG-50.549" in file):

            # convert file to docx, storing it in an untracked folder called temp
            file_docx = file + 'x'
            command = 'textutil -convert docx ' + file + ' -output ' + 'temp/'+ file_docx 
            
            call(command, shell=True)

            # append to the array
            core_doc_asset.append(file_docx)

    os.chdir('temp')

    # get the units for each file, store them and update tracker
    for file in core_doc_asset:
        # get text units for this entry
        units = getTextUnits(file)

        if units:
            # get RG number
            rg_number = file.split("_")[0]

            # find last occurrence of '.' and replace it with '*' 
            k = rg_number.rfind(".")
            mongo_rg = rg_number[:k] + "*" + rg_number[k+1:]

            # insert units on the output collection
            h.update_field(DB, OUTPUT, "shelfmark", mongo_rg, "structured_transcript", units)

            original_filename = file[:-1]
            # update status on the stracker
            h.update_field(DB, TRACKER, "microsoft_doc_file", original_filename, "status", "Processed")

    # success
    pprint.pprint("Core_docx_asset was successfully processed.")

if __name__ == "__main__":
    createStructuredTranscriptDocx()
    #getTextUnits()
    """
    result = h.query(DB, OUTPUT, { "structured_transcript": {'$exists': 'true'}}, {'id': 0})
    pprint.pprint(result)
    """
