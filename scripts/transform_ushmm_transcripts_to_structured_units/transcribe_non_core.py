import sys, glob, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h

os.chdir("../../data/")
from docx import Document
from collections import defaultdict
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
    
    unit_tracker = defaultdict(int)
    
    non_units = ["name:", "date:", "thesis:", "currently:", "note", "comment", "grandparents:", "transcript:", "note:"]

    # iterate over all paragraphs to get text units
    for para in doc.paragraphs:
        paragraph = para.text
        
        # ensure it is not an empty line
        if paragraph:
            # get first word
            unit_type = paragraph.partition(' ')[0]
            # in case it is in the format of e.g 'George Salton:'
            
            # e.g AJ:, B.
            m = re.compile('[A-Z][A-Z]?[.|:|-]')
            type1 = m.match(unit_type)

            # e.g [WJ]
            n = re.compile('\[[A-Z][A-Z]\]')
            typer2= n.match(unit_type)

            # for interviews that have interviewee name at the beginning of unit
            #if unit_type.isupper() and unit_type.isalpha() and len(unit_type) > 1:

            # else parse them according to formatting guidelines
            if ("Question:" in unit_type or
                type1 or
                "Answer:" in unit_type or 
                typer2):
                
                units.append({'unit': paragraph})
                # update tracker
                unit_tracker[unit_type] += 1

            elif (unit_type.endswith(':') and
                    unit_type.lower() not in non_units and
                    unit_type[:-1].isalpha()):
                
                units.append({'unit': paragraph})
                # update tracker
                unit_tracker[unit_type] += 1
            
            # backup method,in case it is in the format of e.g 'George Salton:'
            elif len(paragraph.split()) > 1:
                backup_type = paragraph.split()[1]
                #print(backup_type)

                if ':' in backup_type and backup_type.lower() not in non_units: 
                    units.append({'unit': paragraph})
                    # update tracker
                    unit_tracker[unit_type] += 1

            elif len(paragraph.split()) > 2:
                backup_type = paragraph.split()[2]
                
                if filename == "RG-50.470.0012_trs_en.docx":
                    print backup_type
                if ':' in backup_type and backup_type.lower() not in non_units: 
                    units.append({'unit': paragraph})
                    # update tracker
                    unit_tracker[unit_type] += 1
 

    # check if backup method needed
    if len(unit_tracker) == 1:
        print(units)
        print(filename)
        return {}
    return units

def createStructuredTranscriptDocX():
    docx_assets = []
    count = 0
    for file in glob.glob("*.docx"):
         # RG numbers for the non-core asset
        if ("RG-50.030" not in file and
            "RG-50.106" not in file and
            "RG-50.549" not in file):
            docx_assets.append(file)

    # get the units for each file, store them and update tracker
    for file in docx_assets:
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

            # update status on the stracker
            h.update_field(DB, TRACKER, "microsoft_doc_file", file, "status", "Processed")
        else:
            count += 1
            #print(file)
    print count

    # success
    pprint.pprint("Core_docx_asset was successfully processed.")
    

if __name__ == "__main__":
    createStructuredTranscriptDocX()