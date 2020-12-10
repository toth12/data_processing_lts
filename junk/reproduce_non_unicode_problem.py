import os,sys


helper_path = os.getcwd()+"/utils"
sys.path.insert(0, helper_path)



import pdb  

import glob
import csv
#import helper_mongo as h
import codecs
import constants
from text import transform_fields_with_non_latin_characters_to_latin
import codecs
import pandas as pd

##
# Globals
##

# inputs and global config
INPUT_DATA = constants.INPUT_FOLDER_USC_METADATA+'transcript_testimonies_info_for_Gabor.csv' # path to metadata xml
db = constants.DB# the database name to use when saving results
OUTPUT_COLLECTION = constants.OUTPUT_COLLECTION_USC


fieldname_map={'IntCode':'testimony_id','IntervieweeName':'interviewee_name','Gender':'gender','Shelfmark':'shelfmark','CollectionOwner':'collection'}


def rename_usc_metadata_fields():
    
    #open the input file and make a python dictionary out of it


    # Fix 1:
    
    INPUT_DATA = '/Users/gmt28/Documents/Workspace/lts-data-processing/shoah-foundation-data/data/inputs/usc/metadata/metadata_final_2.csv'
    data=pd.read_csv(INPUT_DATA)
    print (data.iloc()[10]['ghetto_names'])
    
    pdb.set_trace()
    # Fix 1 ends
    f=codecs.open(INPUT_DATA, encoding='utf-8',errors='ignore')
    reader = csv.DictReader(f)
    data_with_renamed_fields=[]
    


    for line in reader:
        #change the fieldnames and build a new dictionary
        new_entry={}
        for key in line:
            if key not in fieldname_map.keys():
                new_entry[key]=line[key]
            else:
                new_entry[fieldname_map[key]]=line[key]
            #add a missing field
        new_entry['recording_year']=int(new_entry['recording_year'])
        data_with_renamed_fields.append(new_entry)
    
    return data_with_renamed_fields

def post_process_ghetto_names(names):
    result=[]
    if len(names)>0:
        individual_names=names.strip().split(';')
        for element in individual_names:
            if len(element)>0:
                name=element.split('(')[0].strip()
                result.append(name)
    return result

def post_process_camp_names(names):
    result=[]
    if len(names)>0:
        individual_names=names.strip().split(';')
        for element in individual_names:
            if 'Concentration Camp)' in element or 'Death Camp)' in element:
                name=element.split('(')[0].strip()
                if len(name)>2:
                    result.append(name)
    return result




def post_process_metadata(meta_data):

    for element in meta_data:
        #postprocess ghetto names
        element['ghetto_names']=post_process_ghetto_names(element['ghetto_names'])
        element['camp_names']=post_process_camp_names(element['camp_names'])
        element['media_url']=[element['media_url']]
        #provenance to be left empty
        element['provenance']=''
        element['interviewee_name']=element['interviewee_name']
        element['shelfmark']='USC SHOAH '+element['testimony_id']
        element['testimony_id']='usc_shoah_'+element['testimony_id']
        element['testimony_title']='Oral history interview with '+element['testimony_title']

        if element['gender']=='M':
            element['gender']='male'
        else:
            element['gender']='female'
    return meta_data








def main():
    #create a collection that will hold the data

    #os.system('mongo ' + db + ' --eval "db.createCollection(\''+OUTPUT_COLLECTION+'\')"')

    usc_metadata_renamed=rename_usc_metadata_fields()
    usc_metadata_processed=post_process_metadata(usc_metadata_renamed)
    
    #problem identification starts
    data=pd.DataFrame(usc_metadata_processed)
    print (data.iloc()[10]['ghetto_names'])
    pdb.set_trace()
    #problem identification finishes
    
    usc_metadata_processed=transform_fields_with_non_latin_characters_to_latin(usc_metadata_processed)

    
    #upload result
    #h.insert(db,OUTPUT_COLLECTION,usc_metadata_processed)

if __name__ == '__main__':
    main()
