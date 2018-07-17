from create_folia_xml_with_divisions import process as create_folia_xml_with_divisions
from annotate_folia_file import annotate
from sentence_divide_annotate_folia_divisions import process as sentence_divide_annotate_folia_divisions
from create_html_output import process as create_html_output
from create_token_sentence_lookup import process as create_token_sentence_lookup
from stanfordcorenlp import StanfordCoreNLP
import pdb
import os
import json
import sys
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
import corenlp
import constants
import random

os.environ["CORENLP_HOME"] = constants.CORENLP_HOME


DB=constants.DB

folia_output_folder=constants.FOLIA_OUTPUT_FOLDER


def process(data):
    
    try:
        
        folia_xml_with_divisions=create_folia_xml_with_divisions(data)
        annotated_folia_xml=sentence_divide_annotate_folia_divisions(folia_xml_with_divisions,'s')
        
        html_output=create_html_output(annotated_folia_xml)
        look_up_table=create_token_sentence_lookup(annotated_folia_xml,data['testimony_id'])
        h.update_entry('let_them_speak_data_processing_test', 'testimonies',data['_id'],{'html_transcript':html_output}) 
        h.insert('let_them_speak_data_processing_test', 'tokens',look_up_table)

        annotated_folia_xml.save(folia_output_folder+data['testimony_id']+'.xml')
       
        
    except:
        e = sys.exc_info()
        print e        
        return data['shelfmark']

    
            
    

def main():
    
    

    #start Stanford Parser in the background

    


    problematic_ids=[]


    
    results=h.query(DB, 'testimonies', {'structured_transcript':{'$exists':True}}, {'testimony_id':1,'structured_transcript':1,'shelfmark':1,'collection':1,'camp_names':1,'ghetto_names':1,'gender':1,'interviewee_name':1,'recording_year':1} )   
    
    
    
    
    for index,result in enumerate(results):
        
        
       
        print "The folia processing of "+str(index)+". document out of "+str(len(results))+" started."
        element=process(result)
        if element is not None:

            problematic_ids.append(element)

                
            
    
    print ("From the following shelfmarks a folia file could not be created; it is logged into: "+constants.FOLIA_PROCESSING_LOG_FOLDER)
    
    print('\n'.join(problematic_ids))
    
    #write the missing files to text file
    file = open(constants.FOLIA_PROCESSING_LOG_FOLDER+'unprocessed_shelfmarks.txt','w')
    file.write('\n'.join(problematic_ids))

    

    
    


    
