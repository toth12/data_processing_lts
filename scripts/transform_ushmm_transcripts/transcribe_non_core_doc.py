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

def get462Monologue(filename):
    """
    Returns the units for the 3 intervies undeviews under the RG-50.005 series
    This series is composed of monologues with some sentences randomly separated 
    by line breaks
    """
    doc = Document(filename)

    monologue = ""
    for para in doc.paragraphs:
        paragraph = para.text
        
        # ensure it is not an empty line
        if (len(paragraph) > 0) and len(paragraph.split()) > 7:
            # add to monologue
            monologue += ' ' + paragraph

    return list({'unit': monologue})

def getUnstructured042Units(filename):
    """
    Returns the unstructured units of the RG.50-402 series
    These interviews did not have any indi
    """
    doc = Document(filename)
    units = list()
    # all interviews start with a header
    isHeader = True
    # iterate over all paragraphs to get text units
    for para in doc.paragraphs:
        paragraph = para.text
        
        # ensure paragraph is not just empty line
        hasText = paragraph.lstrip()
        # ensure it is not an empty line
        if hasText:

            if isHeader:
                if 'beep' in paragraph.lower():
                    isHeader = False
            else:
                # marks the end of the interview
                if 'USHMM Archives' in paragraph or "wentworth films" in paragraph.lower() :
                    break
                elif 'beep' not in paragraph.lower():
                   units.append({'unit':paragraph})
    
    return units


def getUnstructured042_special_Units(filename):
    """
    Returns the unstructured units of the RG.50-402 series
    These interviews did not have any indi
    """
    doc = Document(filename)
    units = list()
    # all interviews start with a header
    isHeader = True
    # iterate over all paragraphs to get text units
    for para in doc.paragraphs:
        paragraph = para.text
        
        # ensure paragraph is not just empty line
        hasText = paragraph.lstrip()
        # ensure it is not an empty line
        if hasText:

            
            units.append({'unit':paragraph})
    return units

def get926Monologue(filename):
    """
    Returns the unstructured units of the RG.50-402 series
    These interviews did not have any indi
    """
    doc = Document(filename)
    monologue = ""
    o = re.compile('track [0-9][0-9]')

    # iterate over all paragraphs to get text units
    for para in doc.paragraphs:
        paragraph = para.text

        # timestamp e.g 15:01:27
        isHeader = o.match(paragraph.lower())         
        # ensure paragraph is not just empty line
        hasText = paragraph.lstrip()

        # ensure it is not an empty line
        if hasText and not isHeader:
            monologue += paragraph
        
    return [{'unit': monologue}]


def getUnstructured_50_233_0083_Units(filename):
    """
    Returns the unstructured units of the RG.50-233-0083 documents
    These interviews did not have any indi
    """
    doc = Document(filename)
   
    
    units=[]
    # iterate over all paragraphs to get text units
    for para in doc.paragraphs:
        paragraph = para.text
        if len(paragraph.strip())>0:
            units.append({'unit':paragraph.strip()})

        
    
    return units
def getUnstructured926Units(filename):
    """
    Returns the unstructured units of the RG.50-402 series
    These interviews did not have any indi
    """
    doc = Document(filename)
    units = list()
    n = re.compile('track [0-9][0-9]')

    # iterate over all paragraphs to get text units
    for para in doc.paragraphs:
        paragraph = para.text
        
        # ensure paragraph is not just empty line
        hasText = paragraph.lstrip()
        # ensure it is not an empty line
        if hasText:
            isHeader = n.match(paragraph.lower())

            # marks the end of the interview
            if "story preservation initiative" in paragraph.lower() or "copyright" in paragraph.lower() :
                break
            elif not isHeader:
                units.append({'unit':paragraph})
    # in case it is a monologue
    if not units:
        units = get926Monologue(filename)

    return units
def getTextUnits_old(filename):
    """
    Returns the text units for a given file in the non-core asset
    Uses regex to identify common patterns and uses specific backup methods
    depending on the interview shelfmark series, in case they are highly
    unstructured
    """
    doc = Document(filename)
    units = list()
    
    unit_tracker = defaultdict(int)
    
    non_units = ["name:", "date:", "date", "series", "transcriber", "thesis:", "currently:", "note", "comment", "grandparents:", "transcript:", "note:"]

    ongoing_answer = ""

    

    # iterate over all paragraphs to get text units
    for para in doc.paragraphs:
        paragraph = para.text
        # ensure it is not an empty line
        if len(paragraph.strip())>0:
            # get first word
            formatted_para = paragraph.lstrip()
            unit_type = formatted_para.partition(' ')[0]
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

                # check if there was an ongoing paragraph
               #units.append({'unit': paragraph})
                
                if ongoing_answer: 
                    units.append({'unit': ongoing_answer})

                # reset it
                ongoing_answer = ""
                ongoing_answer += paragraph
                
                # update tracker
                unit_tracker[unit_type] += 1

            elif (unit_type.endswith(':') and
                    unit_type.lower() not in non_units and
                    unit_type[:-1].isalpha()):
                
                
                units.append({'unit': paragraph})
                # update tracker
                unit_tracker[unit_type] += 1
            
            
            # backup method,in case it is in the format of e.g 'George Salton:'
            elif len(paragraph.split()) > 3:
                backup_type = paragraph.split()[1]
                backup_two = paragraph.split()[2]

                if ((':' in backup_type or backup_type.lower() not in non_units) or
                    (':' in backup_two or backup_two.lower() not in non_units)): 
                    
                    if ((paragraph.strip()[0].islower() and len(paragraph.strip()) > 5) or (paragraph.strip()[-1] in ['.','!','?'])) and len(units) >0:
                        units[-1]['unit']=units[-1]['unit']+ ' '+paragraph
                    # update tracker
                        unit_tracker[unit_type] += 1
                    else:
                        units.append({'unit':paragraph})
                        unit_tracker[unit_type] += 1
            # if it is none of these cases, maybe there is an ongoing answer
                
            elif (ongoing_answer and ongoing_answer != paragraph):
               
                if not any(non_unit in paragraph.lower() for non_unit in non_units):
                    ongoing_answer += paragraph
            else:
                units.append({'unit':paragraph})

    if len(unit_tracker) < 2:
        return []
    
    return units

def createStructuredTranscript_Non_Core_Doc():
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
        '''if ("RG-50.030" not in file and
            "RG-50.106" not in file and
            "RG-50.549" not in file):
        '''
        if (('50.042.0025' in file) or ('50.042.0012' in file) or ('50.042.0014' in file)):

           
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
    for mongo_rg in core_doc_asset:
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
   