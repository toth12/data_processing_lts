import sys, glob, os
root_path = os.path.join("..", "..")
sys.path.insert(0, root_path)
from docx import Document
from subprocess import call

import pprint
import constants
import re
import pdb
import os,sys
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
import text
import folia_utils
import pdb
from data_spec import create_dictionary_of_file_list


import constants
from string import Template
import commands
import heapq

DB=constants.DB
TRACKER="USHMM_transcript_processing_progress_test"
SAMPLE_FILE='sample_data/input_ids.txt'
INPUT_FOLDER='/Users/gmt28/Documents/Workspace/Docker_Engine/varad/Yale_Projects/shoah-foundation-data-restored/shoah-foundation-data/data/inputs/ushmm/transcripts/microsoft_doc_docx/'

def getTextUnits(filename):
    doc = Document(filename)
    units = list()

    #Check if any known segmentation unit is available
    regex_units=r'track [0-9][0-9]',r'[A-Z][A-Z]?[.|:|-]',r'[0-9]?[0-9]:[0-9][0-9]:[0-9][0-9]',r'\[[A-Z][A-Z]\]'
    question_units=["Question:","Q:","Q."]
    answer_units=["Answer:",'A:','A.']
    non_units = ["name:", "date:", "date", "series", "transcriber", "thesis:", "currently:", "note", "comment", "grandparents:", "transcript:", "note:"]

      

    text = ' '.join([' '.join(para.text.split()[0:4]) for para in doc.paragraphs if len(para.text.strip()) >50])
    counter=text.split()

    result_counter=[]
    for element in question_units:
        result_counter.append(counter.count(element))
    question_units_present=heapq.nlargest(1, result_counter)

    result_counter=[]
    for element in answer_units:
        result_counter.append(counter.count(element))
    answer_units_present=heapq.nlargest(1, result_counter)

    result_counter=[]
    if (question_units_present[0]==0 and answer_units_present[0]==0):
        for element in regex_units:
            pattern=re.compile(element)
            pattern_presence= pattern.findall(text)
            result_counter.append(len(pattern_presence))
    result_counter.index(heapq.nlargest(1, result_counter)[0])
    pdb.set_trace()
    # iterate over all paragraphs to get text units
    for para in doc.paragraphs:
        paragraph = para.text
        
        # ensure it is not an empty line
        if len(paragraph.strip())>0:
            # get first word
            print 'l'
    return units


if __name__ == '__main__':
    
    ids=open(SAMPLE_FILE).readlines()
    all_files=[]
    for testimony_id in ids[0:1]:

        result=h.query(DB,TRACKER,{'id':testimony_id.strip()},{'microsoft_doc_file':1,'method':1,'id':1,'_id':0})[0]
        all_files.append(result)

    for element in all_files:

        name=element['microsoft_doc_file'][0]
        if name.split('.')[-1]=='doc':
            for files in element['microsoft_doc_file']:
                
                file=INPUT_FOLDER+ files
                command = 'textutil -convert docx ' + file + ' -output ' + os.getcwd()+'/sample_data/'+files+'x' 
                file=os.getcwd()+'/sample_data/'+files+'x'
                getTextUnits(file)
        else:
            for file in element['microsoft_doc_file']:
                file=INPUT_FOLDER+file
                getTextUnits(file)
    
            



    '''
unit_type = paragraph.partition(' ')[0]

            # exception, two interviews do not follow the formatting guidelines
            # handle them
            if ("RG-50.030.0710_trs_en.docx" in filename or
                "RG-50.030.0711_trs_en.docx" in filename):
                
                if unit_type == "[DL]" or unit_type == "[AG]" or unit_type== "[BB]":
                    units.append({'unit': paragraph})
            
            # else parse them according to formatting guidelines
            elif ("Question:" in unit_type or
                unit_type == "Q:" or
                "Q." in unit_type or
                "Answer:" in unit_type or 
                unit_type == "A:" or
                "A." in unit_type):

                units.append({'unit': paragraph})

    '''