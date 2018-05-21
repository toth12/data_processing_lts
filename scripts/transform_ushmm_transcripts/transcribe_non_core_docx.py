import sys, glob, os
import helper_mongo as h


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

def get062Monologue(filename):
    """
    Returns the monologue unit for the RG-50.062 series
    Ignores headers info annotated within -- or ..
    """
    doc = Document(filename)
    
    monologue = ""
    
    # ignore all the -TITLE
    # iterate over all paragraphs to get text units
    for para in doc.paragraphs:
        paragraph = para.text
        
        # ensure it is not an empty line
        if paragraph:
            
            # ensure it is not a header type
            if paragraph.count('-') < 2 and paragraph.count('.') < 2:
                monologue += paragraph
    
    return list({'unit': monologue})

def getUnstructured203Units(filename):
    """
    Returns the units for the RG-50.203  interviews
    Ignores the first page that consists of interview header info
    """
    doc = Document(filename)
    units = list()
    isHeader = True
    for para in doc.paragraphs:
        paragraph = para.text
        
        # ensure it is not an empty line
        if paragraph:

            # ignore the initial header info
            if isHeader:
                if paragraph.split() > 5:
                    units.append(paragraph)
                    isHeader = False

            else:
                units.append({'unit': paragraph})

    return units   

def get405Monologue(filename):
    """
    Returns the monologue unit for the RG-50.405 monologue interviews
    Ignores the first page that consists of interview header info
    """
    doc = Document(filename)
    units = list()
    isHeader = True
    monologue = ""
    for para in doc.paragraphs:
        paragraph = para.text
        
        # ensure it is not an empty line
        if paragraph:
            if isHeader:
                # this strings indicates wheen the end of the headeer
                if "JEWISH ORGANIZATIONAL AFFILIATIONS (IF GIVEN):" in paragraph:
                    isHeader = False
            
            else:
                monologue += paragraph
    units.append({'unit:': monologue})

    return units

def getUnstructured405Units(filename):
    """
    Returns the units for the highly irregular RG-50.405 series
    Questions and answers were on the same paragraph.
    Questions were annotated within a parethensesis e.g. (Where do you live?)
    Some answers for the same questions were broken in different paragraphs
    """
    doc = Document(filename)
    units = list()
    isHeader = True

    ongoing_answer = ""
    for para in doc.paragraphs:
        paragraph = para.text
        
        # ensure it is not an empty line
        if paragraph:
            # check if there is a question
            para_partition = paragraph.split(')', 1)
            
            # it is a Q & A
            if isHeader:
                # check if we found the start of the interview - first question
                if (len(para_partition) > 1 and 
                    para_partition[0][len(para_partition[0]) - 1] == '?'):
                    # ignore the initial ? for the question
                    units.append({'unit': para_partition[0][1:]})

                    # start capturing the answer
                    ongoing_answer += para_partition[1].lstrip()
                    #units.append({'unit:': para_partition[1]})
                    isHeader = False
            else:
                # found a new question
                if (len(para_partition) > 1 and 
                    para_partition[0][len(para_partition[0]) - 1] == '?'):
                    # save the previous answer if any
                    if ongoing_answer:
                        units.append({'unit': ongoing_answer})

                    # reset it
                    ongoing_answer = ""
                    
                    # get question
                    question = para_partition[0].lstrip() 

                    # ignore the initial '(' for the question
                    units.append({'unit': question[1:]})

                    #units.append({'unit:': para_partition[1]})
                    ongoing_answer +=  para_partition[1].lstrip()
                else:
                    ongoing_answer +=  paragraph.lstrip()

    
    # in case it is a monologue
    if len(units) < 5:
        units = get405Monologue(filename)
        
    return units

"""
def getUnstructured005Units(filename):
    doc = Document(filename)
    units = list()
    isHeader = True

    for para in doc.paragraphs:
        paragraph = para.text
        
        # timestamp e.g 15:01:27
        o = re.compile('[0-9]?[0-9]:[0-9][0-9]:[0-9][0-9]')
        # ensure it is not an empty line
        if paragraph:
            if isHeader:
"""
def getBasicMonologue(filename):
    """
    Returns the units for the 3 intervies undeviews under the RG-50.005 series
    This series is composed of monologues with some sentences randomly separated 
    by line breaks
    """
    doc = Document(filename)
    isHeader = True

    monologue = ""
    for para in doc.paragraphs:
        paragraph = para.text
        
        # ensure it is not an empty line
        if paragraph:
            if isHeader:
                if len(paragraph.split()) > 7:
                    isHeader = False
                    monologue += paragraph
            else:
                monologue += ' ' + paragraph

    return list({'unit': monologue})
            

def getTextUnits(filename):
    """
    Returns the text units for a given file in the non-core asset
    Uses regex to identify common patterns and uses specific backup methods
    depending on the interview shelfmark series, in case they are highly
    unstructured
    """
    doc = Document(filename)
    units = list()
    
    unit_tracker = defaultdict(int)
    
    non_units = ["name:", "date:", "thesis:", "currently:", "note", "comment", "grandparents:", "transcript:", "note:"]

    #  50.005 is a special case, with line breaks for every sentence

    
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

            # timestamp e.g 15:01:27
            o = re.compile('[0-9]?[0-9]:[0-9][0-9]:[0-9][0-9]')
            type3 = o.match(unit_type)           

            # else parse them according to formatting guidelines
            if ("Question:" in unit_type or
                type1 or
                "Answer:" in unit_type or 
                typer2 or
                type3):

                safePrint(unit_type)
                units.append({'unit': paragraph})
                # update tracker
                unit_tracker[unit_type] += 1

            elif (unit_type.endswith(':') and
                    unit_type.lower() not in non_units and
                    unit_type[:-1].isalpha()):
                
                safePrint(unit_type)
                units.append({'unit': paragraph})
                # update tracker
                unit_tracker[unit_type] += 1
            
            # backup method,in case it is in the format of e.g 'George Salton:'
            elif len(paragraph.split()) > 3:
                backup_type = paragraph.split()[1]
                backup_two = paragraph.split()[2]

                safePrint(backup_type)

                if ((':' in backup_type and backup_type.lower() not in non_units) or
                    (':' in backup_two and backup_two.lower() not in non_units)): 
                    units.append({'unit': paragraph})
                    # update tracker
                    unit_tracker[unit_type] += 1
 

    # apply backup method when needed
    if len(unit_tracker) < 2:
        # the remaining 50.062 series is composed of monologues
        if "RG-50.062" in filename:
            units = get062Monologue(filename)
            return units
        
        elif "RG-50.233" in filename:
            units = getUnstructured203Units(filename)

        elif "RG-50.405" in filename:
            units = getUnstructured405Units(filename)
        
        elif ("RG-50.043" in filename or 
            "RG-50.462" in filename or
            "RG-50.045" in filename):
            units = getBasicMonologue(filename)
        else:
            return []

    #if "005.0028" in filename:
        #pprint.pprint(units)
    return units

    
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
    for file in docx_assets:
        # get text units for this entry
        units = getTextUnits(file)

        if units:
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
            h.update_field(DB, TRACKER, "microsoft_doc_file", original_filename, "extraction_method", "transcribe_non_core_docx")

        else:
            missing_count += 1
            missing_files.append(file.split('/')[-1])
            print(file)
    
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