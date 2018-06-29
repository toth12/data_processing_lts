import sys, os
import pdb
#set utils path
helper_path = os.getcwd()+"/utils"
sys.path.insert(0, helper_path)
import helper_mongo as h

#set constants path
constants_path = os.getcwd()
sys.path.insert(0, constants_path)
import constants
import csv




##Global Variables##



output_db=constants.OUTPUT_DB
input_db=constants.DB
output_folder=constants.OUTPUT_FOLDER_FOR_QUALITY_CONTROL




def replace_transcript():
	ids=h.query('lts','testimonies_for_quality_control',{},{'testimony_id':1})
	for i in ids:
		new_transcript=h.query('lts','testimonies',{'testimony_id':i['testimony_id']},{'html_transcript':1})[0]['html_transcript']
		h.update_entry('lts','testimonies_for_quality_control',i['_id'],{'html_transcript':new_transcript})
		
if __name__ == '__main__':

	#duplicate the testimonies db 
	replace_transcript()