import sys, glob, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h

os.chdir("../../data/")
from docx import Document
import pprint
import constants

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
            
            if (unit_type == "Question:" or
                unit_type == "Q:" or
                unit_type == "Answer:" or 
                 unit_type == "A:"):
                units.append({'unit':paragraph})
            
    return units

def createStructuredTranscriptDocx():
    """
    Processes the 82 docx files beloging to the core asset in data
    Core asset is identified by numbers RG-50.030, RG-50.106, RG-50.549
    """
    core_docx_asset = []

    # get all the docx files that are part of the core asset
    for file in glob.glob("*.docx"):

        # RG numbers for the core asset
        if ("RG-50.030" in file or
            "RG-50.106" in file or
            "RG-50.549" in file):
            # append to the array
            core_docx_asset.append(file)

    # get the units for each file, store them and update tracker
    for file in core_docx_asset:
        # get text units for this entry
        units = getTextUnits(file)
        
        # get RG number
        rg_number = file.split("_")[0]

        # find last occurrence of '.' and replace it with '*' 
        k = rg_number.rfind(".")
        mongo_rg = rg_number[:k] + "*" + rg_number[k+1:]

        # insert units on the output collection
        h.update_field(DB, OUTPUT, "shelf_mark", mongo_rg, "structured_transcript", units)

        # update status on the stracker
        h.update_field(DB, TRACKER, "microsoft_doc_file", file, "status", "Processed")

    # success
    pprint.pprint("Core_docx_asset was successfully processed.")

if __name__ == "__main__":
    createStructuredTranscriptDocx()
    """
    result = h.query(DB, OUTPUT, { "structured_transcript": {'$exists': 'true'}}, {'id': 0})
    pprint.pprint(result)
    """
