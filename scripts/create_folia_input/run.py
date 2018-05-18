from create_folia_xml_with_divisions import process as create_folia_xml_with_divisions
from annotate_folia_file import annotate
from sentence_divide_folia_divisions import process as sentence_divide_folia_divisions
from create_html_output import process as create_html_output
from create_token_sentence_lookup import process as create_token_sentence_lookup

'''
from tokenize_folia_file import process as tokenize_folia_file
from pos_tag_folia_file import process as pos_tag_folia_file

from create_token_sentence_lookup import process as create_token_sentence_lookup
from components import postagger_component as pt
'''
import pdb
import os
import json
import sys
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
import corenlp
os.environ["CORENLP_HOME"] = r'/Users/gmt28/Documents/Workspace/Docker_Engine/varad/Yale_Projects/shoah-foundation-data-restored/shoah-foundation-data/lib/stanford-corenlp-full-2018-02-27'
import constants


def process(data,id_,_id,shelf_mark,client):

    try:
        folia_xml_with_divisions=create_folia_xml_with_divisions(data,id_,shelf_mark,'1923','Budapest','Birkenau','M')
        folia_xml_with_sentences=sentence_divide_folia_divisions(folia_xml_with_divisions,'s')
        annotated_folia_xml=annotate(folia_xml_with_sentences,client)
        html_output=create_html_output(annotated_folia_xml)
        look_up_table=create_token_sentence_lookup(annotated_folia_xml,id_)
        h.update_entry('let_them_speak_data_processing_test', 'testimonies',_id,{'html_transcript':html_output}) 
        h.insert('let_them_speak_data_processing_test', 'tokens',look_up_table)

        annotated_folia_xml.save(constants.FOLIA_OUTPUT_FOLDER+id_+'.xml')

    except:
        e = sys.exc_info()
        print e        
        return shelf_mark

    
            
    

def main():
    
    


    #get the id of those documents that has a structured_transcript field
    #todo use constants here
    #todo: work on a better parser
    

    #start Stanford Parser in the background

    with corenlp.CoreNLPClient(annotators="tokenize ssplit pos lemma".split(),properties={'timeout': '50000'}) as client:


        problematic_ids=[]
        
        results=h.query('let_them_speak_data_processing_test', 'testimonies', {'structured_transcript':{'$exists':True}}, {'testimony_id':1,'structured_transcript':1,'shelfmark':1} )   
        
        #results=h.aggregate('let_them_speak_data_processing_test', 'testimonies',     [{ '$sample': {'size': 10} }, { '$project' : {'testimony_id':1,'structured_transcript':1,'shelfmark':1} } ] )   

        for index,result in enumerate(results[0:1]):
            
            print (index)
             
            element=process(result['structured_transcript'],result['testimony_id'],result['_id'],result['shelfmark'],client)
            if element is not None:
                problematic_ids.append(element)
    
    print ("From the following shelfmarks a folia file could not be created; it is logged into: "+constants.FOLIA_PROCESSING_LOG_FOLDER)
    
    print('\n'.join(problematic_ids))

    #write the missing files to text file
    file = open(constants.FOLIA_PROCESSING_LOG_FOLDER+'unprocessed_shelfmarks.txt','w')
    file.write('\n'.join(problematic_ids))

    #unidecode.unidecode(text)
    


    '''
    #load the sample data
    
    with open(os.getcwd()+'/data/input/sample_input.json') as json_data:
        sample_data = json.load(json_data)
    process(sample_data,'some_id',pos_tagger,'someid','someshelfmark')

    '''
