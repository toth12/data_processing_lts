import sys, glob, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h


from docx import Document
import pprint
import constants

TRACKER = constants.USHMM_TRACKER_COLLECTION
OUTPUT = constants.OUTPUT_COLLECTION_USHMM
DB = constants.DB
INPUT_FOLDER=constants.INPUT_FOLDER_USHMM_TRANSCRIPTS_DOC

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

            # exception, two interviews do not follow the formatting guidelines
            # handle them
            if (filename == "RG-50.030.0710_trs_en.docx" or
                filename == "RG-50.030.0711_trs_en.docx"):
                
                if unit_type == "[DL]" or unit_type == "[AG]":
                    units.append({'unit': paragraph})
            
            # else parse them according to formatting guidelines
            elif ("Question:" in unit_type or
                unit_type == "Q:" or
                "Q." in unit_type or
                "Answer:" in unit_type or 
                unit_type == "A:" or
                "A." in unit_type):

                units.append({'unit': paragraph})

    return units

def createStructuredTranscriptDocx():
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
            # append to the array
            core_docx_asset.append(file)

    # get the units for each file, store them and update tracker
    for file in core_docx_asset:
        # get text units for this entry
        units = getTextUnits(file)
       
        # get RG number
        original_filename = file.split('/')[-1]
        rg_number=original_filename.split("_")[0]

        # find last occurrence of '.' and replace it with '*' 
        k = rg_number.rfind(".")
        mongo_rg = rg_number[:k] + "*" + rg_number[k+1:]

        # insert units on the output collection
        h.update_field(DB, OUTPUT, "shelfmark", mongo_rg, "structured_transcript", units)

        # update status on the stracker
        h.update_field(DB, TRACKER, "microsoft_doc_file", original_filename, "status", "Processed")
        
    # success
    pprint.pprint("Core_docx_asset was successfully processed.")

if __name__ == "__main__":
    createStructuredTranscriptDocx()
    """
    result = h.query(DB, OUTPUT, { "structured_transcript": {'$exists': 'true'}}, {'id': 0})
    pprint.pprint(result)
    """
