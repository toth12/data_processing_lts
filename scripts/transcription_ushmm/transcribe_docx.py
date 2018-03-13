import sys, glob, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h

os.chdir("../../data/")
from docx import Document
import pprint

TRACKER = "USHMM_transcript_processing_progress"
DB = "Hol"

def getTextUnits(filename):
    doc = Document(filename)
    
    questions_doc = []
    answers_doc = []

    # iterate over all paragraphs to get text units
    for para in doc.paragraphs:
        paragraph = para.text
        
        # ensure it is not an empty line
        if paragraph:
            # get first word
            unit_type = paragraph.partition(' ')[0]
            
            if (unit_type == "Question:" or
                unit_type == "Q:"):
                questions_doc.append(paragraph)
            
            elif (unit_type == "Answer:" or 
                 unit_type == "A:"):
                answers_doc.append(paragraph)
            
    return questions_doc, answers_doc

if __name__ == "__main__":

    core_docx_asset = []

    # get all the docx files that are part of the core asset
    for file in glob.glob("*.docx"):

        # RG numbers for the core asset
        if ("RG-50.030" in file or
            "RG-50.106" in file or
            "RG-50.549" in file):
            # append to the array
            core_docx_asset.append(file)

    for file in core_docx_asset:
        # get text units for this entry
        question_docs, answers_doc = getTextUnits(file)

        # update status
        h.update_status(DB, TRACKER, "microsoft_doc_file", file, "Processed")
    
    result = h.query(DB, TRACKER, {}, {'id': 0})
    pprint.pprint(result)