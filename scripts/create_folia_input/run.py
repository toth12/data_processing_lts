from create_folia_xml_with_divisions import process as create_folia_xml_with_divisions
from annotate_folia_file import annotate
from sentence_divide_folia_divisions import process as sentence_divide_folia_divisions
'''
from tokenize_folia_file import process as tokenize_folia_file
from pos_tag_folia_file import process as pos_tag_folia_file
from create_html_output import process as create_html_output
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


from print_xml import pretty_print
def process(data,id_,_id,shelf_mark):
    #try:
    folia_xml_with_divisions=create_folia_xml_with_divisions(data,id_,shelf_mark,'1923','Budapest','Birkenau','M')
        

    folia_xml_with_sentences=sentence_divide_folia_divisions(folia_xml_with_divisions,'s')
       
    annotated_folia_xml=annotate(folia_xml_with_sentences)
    pdb.set_trace()

    '''

        folia_xml_with_tokens=tokenize_folia_file(folia_xml_with_sentences)
       
        #result 1 to be written out to file
        folia_xml_pos_tagged=pos_tag_folia_file(folia_xml_with_tokens,pos_tagger)

        #result 2 to be pushed to the DB
        html_output=create_html_output(folia_xml_pos_tagged)

        #result 3 to be pushed to the DB

        look_up_table=create_token_sentence_lookup(folia_xml_pos_tagged,id_)

        #insert the html text
        h.update_entry('let_them_speak_data_processing_test', 'output_ushmm_metadata',_id,{'html_transcript':html_output}) 

        #insert the lookup table
        h.insert('let_them_speak_data_processing', 'tokens',look_up_table)

        
        folia_xml_pos_tagged.save(os.getcwd()+'/data/folia_output/'+id_+'.xml')
        
               
	   with open(os.getcwd()+"/data/html_output/"+id_+".html", "w") as file:
            file.write(html_output)'''

    '''except:
        e = sys.exc_info()
        print e        
        return shelf_mark'''
    #deletet: irn62053 that was an exception for some reasons: db.output_ushmm_metadata.remove({ "_id" : ObjectId("5ab145d0d6acc27b853f5372")});



if __name__ == "__main__":
    with open(os.getcwd()+'/data/input/sample_input.json') as json_data:
        sample_data = json.load(json_data) 
    result=process(sample_data,'some_id','some_id','some_shelf_mark')
    #get the id of those documents that has a structured_transcript field
    #todo use constants here
    #todo: work on a better parser
    


    '''problematic_ids=[]
    #pos_tagger =pt.TreeTaggerComponent('en')
    results=h.query('let_them_speak_data_processing', 'output_ushmm_metadata', {'structured_transcript':{'$exists':True}}, {'testimony_id':1,'structured_transcript':1,'shelfmark':1} )   
    pdb.set_trace()
    for index,result in enumerate(results[0:10]):
        print index
        element=process(result['structured_transcript'],result['testimony_id'],result['_id'],result['shelfmark'])
        if element is not None:
            problematic_ids.append(element)
    print problematic_ids'''

    
    #load the sample data
    '''
    with open(os.getcwd()+'/data/input/sample_input.json') as json_data:
        sample_data = json.load(json_data)
    process(sample_data,'some_id',pos_tagger,'someid','someshelfmark')'''
