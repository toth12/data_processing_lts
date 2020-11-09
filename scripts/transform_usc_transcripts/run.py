import glob
import pdb	
import os,sys
import helper_mongo as h
import csv
import constants
from parse import transform_transcript_to_structured_unit


##
# Globals
##

db = constants.DB
collection=constants.OUTPUT_COLLECTION_USC
INPUT_FOLDER=constants.INPUT_FOLDER_USC_TRANSCRIPTS
OUTPUT_FOLDER_USC_PROCESSING_LOGS=constants.OUTPUT_FOLDER_USC_PROCESSING_LOGS

def run (debug=False):
	'''This function begins the process described in the Readme of this folder'''
	
	#open the transcript list
	reader = csv.DictReader(open(INPUT_FOLDER+'USC_Shoah_Foundation_Transcripts_list.csv', 'rb'))
	not_processed_files=[]
	not_processed_shelfmarks=[]

	c = 0
	for line in reader:
		#set the debugger
		if (debug == True) and (c==10):
			break
		
		
		number_of_parts=line['NumTapes']
	 	int_code=line['IntCode']
	 	final_result=[]
	 	
	 	c = c+1
		try:
		 	for part in range(1,int(number_of_parts)+1):
		 		input_file=INPUT_FOLDER+int_code+'.'+str(part)+'.xml'
			 	result=transform_transcript_to_structured_unit(input_file)
			 	if part != 1:
					final_result.extend([{'unit':'Change of tape'}])
			 	final_result.extend(result)

			 #upload to the DB
			entry_id=h.query(db,collection,{'testimony_id':'usc_shoah_'+int_code},{})[0]
			h.update_entry(db,collection,entry_id['_id'],{'structured_transcript':final_result})
			 			
		except Exception as e:
			not_processed_shelfmarks.append('USC SHOAH '+int_code)
			not_processed_files.append(int_code+'.'+str(part)+'.xml')
		



		#delete the unprocessed entries

	#h.delete(db,collection,{'structured_transcript': { '$exists': False } })
	print ("The processing of the following shelfmarks was not possible, they are logged into: "+OUTPUT_FOLDER_USC_PROCESSING_LOGS)

	print('\n'.join(not_processed_shelfmarks))
	#write the missing files to text file
	file = open(OUTPUT_FOLDER_USC_PROCESSING_LOGS+'processing_failed_shelfmarks.txt','w')
	file.write('\n'.join(not_processed_shelfmarks))

	print ("The processing of the following files was not possible, they are logged into: "+OUTPUT_FOLDER_USC_PROCESSING_LOGS)

	print('\n'.join(not_processed_files))
	#write the missing files to text file
	file = open(OUTPUT_FOLDER_USC_PROCESSING_LOGS+'processing_failed_files.txt','w')
	file.write('\n'.join(not_processed_files))

		



			 
		
if __name__ == '__main__':
	run()