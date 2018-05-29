import os,sys
import csv
import pdb
import codecs
import pandas
import math
constants_path = os.getcwd()
sys.path.insert(0, constants_path)
import constants
from find_sentence_id import find_sentence_id as find_fragment
from pynlpl.formats import folia


####Globals####

input_fragment_gt=os.getcwd()+"/data/inputs/fragments/fragments_by_gt.csv"
input_fragment_ec=os.getcwd()+"/data/inputs/fragments/fragments_by_ec.csv"
input_fragment_manual_back_up=os.getcwd()+"/data/inputs/fragments/fragments_retrieved_manually.csv"
log_folder=constants.OUTPUT_FOLDER_FRAGMENTS_PROCESSING_LOGS
not_found=[]

def read_csv(filename):
	
	df = pandas.read_csv(filename)
	
	

	return df.T.to_dict().values()

def update_fragments(to_be_updated,base_for_updating):
	
	for i,entry in enumerate(to_be_updated):
		#check if we already know the time 
		print len(str(entry['question_position']))	
	
		if len(str(entry['question_position']))<4:
			#if time is unknown check the time in the other file
			result=[element for element in base_for_updating if element['fragment_identifier']==entry['fragment_identifier']]
			to_be_updated[i]['question_position']=result[0]['question_position']
			to_be_updated[i]['video_filename']=result[0]['video_filename']
			
	
	return to_be_updated

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))    
    return           


def find_fragment_position(records,back_up):
	
	for index,record in enumerate(records):
		print '{number} / {processed}'.format(number=index,processed=len(records))
		#check if the transcript already exist
		transcript_file=constants.FOLIA_OUTPUT_FOLDER+record['ushmm_id']+'.xml'
		if not os.path.exists(transcript_file):
			record['transcript_file_available']=False
			#set here the way Doug says
			record['start_sentence_index']=None
			record['end_sentence_index']=None
		else:
			#open the folia xml and try to locate the folia file
			record['transcript_file_available']=True
			folia_xml=folia.Document(file=transcript_file)
			result=find_fragment(record['label_2'],folia_xml)
			#check if it was possible to find the folia xml

			if result is None:
				
				#try to locate it in the back up file
				manual_info=[element for element in back_up if element['fragment_identifier'] == record['fragment_identifier']]
				if len(manual_info)>0:
					record['start_sentence_index']=manual_info[0]['start_sentence_index']
					record['end_sentence_index']=manual_info[0]['end_sentence_index']
				
				else:
				#if not there log it and set the value for 0
				
					not_found.append(record['fragment_identifier'])
					#check in the back-up data 
					record['start_sentence_index']=None
					record['end_sentence_index']=None
			else:
				record['start_sentence_index']=result['start_sentence_index']
				record['end_sentence_index']=result['end_sentence_index']
	return records
		

if __name__ == '__main__':
	fragments_gt=read_csv(input_fragment_gt)
	fragments_ec=read_csv(input_fragment_ec)
	fragments_back_up=read_csv(input_fragment_manual_back_up)
	result=update_fragments(fragments_gt,fragments_ec)

	#eliminate entries that are to be deleted

	result_updated=[element for element in result if not (element['status'] == 'del')]
	print 'updating fragments finished'
	result_with_fragment_pos=find_fragment_position(result_updated,fragments_back_up)

	print ("The following fragments could not be found, and they are logged to "+log_folder)
	
	print('\n'.join(not_found))

	#write the missing files to text file
	file = open(log_folder+'fragments_not_found.txt','w')
	file.write('\n'.join(not_found))
	

	

	WriteDictToCSV('fragments_with_paragraph_info.csv',result_with_fragment_pos[0].keys(),result_with_fragment_pos)

