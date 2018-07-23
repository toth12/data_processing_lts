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
SAMPLE_FILE='scripts/transform_ushmm_transcripts/sample_data/input_ids.txt'
INPUT_FOLDER='/Users/gmt28/Documents/Workspace/Docker_Engine/varad/Yale_Projects/shoah-foundation-data-restored/shoah-foundation-data/data/inputs/ushmm/transcripts/microsoft_doc_docx/'

def getTextUnits(filename):
    doc = Document(filename)
    units = list()

    #Check if any known segmentation unit is available
    regex_units=[r'track [0-9][0-9]',r'[A-Z][A-Z]?[.|:|-]',r'[0-9]?[0-9]:[0-9][0-9]:[0-9][0-9]',r'\[[A-Z][A-Z]\]']
    question_units=["Question:","Q:","Q."]
    answer_units=["Answer:",'A:','A.']
    non_units = ["name:", "date:", "date", "series", "transcriber", "thesis:", "currently:", "note", "comment", "grandparents:", "transcript:", "note:","Interviewer:","Theodore:","mr.","Mr.","[DL]","[AG]","[BB]"]
    
    for para in doc.paragraphs:
        paragraph = para.text.strip()
         # ensure it is not 
       
        presence_regex_unit=False
        presence_answer_unit=False
        presence_question_unit=False
        if len(paragraph)>0:
            # get first word
            first_words=paragraph[0:10]
            for element in question_units:
                if element in first_words:
                    presence_question_unit=True
                    break
            if presence_question_unit == False:
                for element in answer_units:
                    if element in first_words:
                        presence_answer_unit=True
                        break
            if presence_answer_unit==False:
                for element in regex_units:
                    n = re.compile(element)
                    typer2= n.match(first_words)
                    if typer2 and (first_words not in non_units):
                        presence_regex_unit=True
                        break
            if presence_regex_unit or presence_answer_unit or presence_question_unit:
                units.append({'unit':paragraph})

            elif(len(units)>0 and len(paragraph.split())>3):
                if ((units[-1]['unit'].split()>3) and (units[-1]['unit'][-1] not in ['?','.','!']) ):
                    units[-1]['unit']=units[-1]['unit']+' '+paragraph
                else:
                    units.append({'unit':paragraph})
            else: 
                units.append({'unit':paragraph})




    
    return units


def main():
    ids=open(SAMPLE_FILE).readlines()
    all_files=[]
    for testimony_id in ids:

        result=h.query(DB,TRACKER,{'id':testimony_id.strip()},{'microsoft_doc_file':1,'method':1,'id':1,'_id':0})[0]
        all_files.append(result)

    for element in all_files:
        name=element['microsoft_doc_file'][0]
        print element['id']
        if name.split('.')[-1]=='doc':
            result=[]
            for files in element['microsoft_doc_file']:
                
                file=INPUT_FOLDER+ files
                command = 'textutil -convert docx ' + file + ' -output ' + os.getcwd()+'/sample_data/'+files+'x' 
                file=os.getcwd()+'/scripts/transform_ushmm_transcripts/sample_data/'+files+'x'
                units=getTextUnits(file)
                for i,unit in enumerate(units):
                    units[i]['unit']=' '.join(unit['unit'].split())
                result.extend(units)
            h.update_field(DB, 'output_ushmm_metadata', "testimony_id", element['id'], "structured_transcript", result)

        else:
            result=[]
            for file in element['microsoft_doc_file']:
                file=INPUT_FOLDER+file
                units=getTextUnits(file)
                for i,unit in enumerate(units):
                    units[i]['unit']=' '.join(unit['unit'].split())
                result.extend(units)

            h.update_field(DB, 'output_ushmm_metadata', "testimony_id", element['id'], "structured_transcript", result)

    
            
if __name__ == '__main__':
    main()