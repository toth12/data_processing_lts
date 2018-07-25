import os,sys
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import text
import folia_utils
import pdb
import helper_mongo as h
root_path = os.path.join("..", "..")
sys.path.insert(0, root_path)
import constants
from string import Template
import commands
import random





input_csv='sample_data/quality_control.csv'
path_to_old_folia=os.path.join("..", "..", "data/outputs/folia_output_old/")
path_to_new_folia=os.path.join("..", "..", "data/outputs/folia_output/")
DB=constants.DB
method_collection='USHMM_transcript_processing_progress_test'

def add_additional_data(data,pool='old'):
	new_data=[]
	for index,record in enumerate(data):
		print str(index)+"records ouf of "+str(len(data))+" records have been processed"
		try:
			#rename the id attribute to testimony_id
			if pool == 'new':
				record['testimony_id']=record['id']
				record['data_pool']='second'
				record.pop('id')
			entry=record.copy()
			#Get the number of tokens in the previous folia output
			try:
				counts_previous_folia=get_previous_folia_out(record['testimony_id'])
				entry['token_in_prev_folia']=counts_previous_folia['tokens']
				entry['divs_in_prev_folia']=counts_previous_folia['divisions']
			except:
				entry['token_in_prev_folia']=''
				entry['divs_in_prev_folia']=''

			
			#Get the number of tokens in the current folia
			counts_current_folia=get_current_folia_out(record['testimony_id'])
			entry['token_in_current_folia']=counts_current_folia['tokens']
			entry['divs_in_current_folia']=counts_current_folia['divisions']
			
			#Get the method used for building this file
			try:
				entry['method']=h.query(DB,method_collection,{'id':record['testimony_id']},{'method':1})[0]['method']
			except:
				entry['method']=''

			#Get the number of tokens in the undress experiment
			entry['token_in_undress_experiment']=get_undress_exp_token_count(record['testimony_id'])
			if pool=='old':
				if len(entry['pass or fail'])>0:
					entry['status']='first_qc'
				else:
					entry['status']=''

			else:
				entry['status']=''
			#Get the lenght of videos
			entry['video_lenght']=get_video_length(entry['testimony_id'])

			#update keys in the old data where we have no keys
			if pool =='new':
				#add existing keys to it
				input_data_keys=text.ReadCSVasDict('base_data_for_second_qc.csv')[0].keys()
				existing_keys=entry.keys()
				[entry.update({key:''}) for key in input_data_keys if key not in existing_keys ]
			new_data.append(entry)


		
				
		except Exception as e:
			print e

			print "The following id could not be processed: "+entry['testimony_id']
	

	
	if pool =='new':
		#add it to existing file
		input_data=text.ReadCSVasDict('base_data_for_second_qc.csv')
		input_data.extend(new_data)
		#update keys in the old data where we have no keys
		pdb.set_trace()
		text.write_to_csv(input_data,'base_data_for_second_qc.csv')
	else:
		text.write_to_csv(new_data,'base_data_for_second_qc.csv')


def get_previous_folia_out(testimony_id):
	counts={}

	counts=folia_utils.get_counts(path_to_old_folia+testimony_id+'.xml')

	return counts


def get_current_folia_out(testimony_id):
	counts=folia_utils.get_counts(path_to_new_folia+testimony_id+'.xml')
	return counts

def get_undress_exp_token_count(testimony_id):
	#connect to mongo

	result=h.query(DB,'undress',{'id':testimony_id},{'sentence_segmented_tokenized':1})[0]
	data=result['sentence_segmented_tokenized']
	count=sum(len(sentence) for sentence in data)
	return count
def get_video_length(testimony_id):
	#get videos
	videos=h.query('lts','testimonies',{'testimony_id':testimony_id},{'media_url':1})[0]['media_url']
	if len(videos)>0:
		complete_duration=[]
		for video in videos:
			command_to_get_duration= "ffmpeg -i '"+video+"' 2>&1 | grep Duration | awk '{print $2}' | tr -d ,"
			
			## run it ##
			duration=commands.getoutput(command_to_get_duration)
			complete_duration.append(get_sec(duration))
		complete_duration=sum(element for element in complete_duration)
	else:
		complete_duration=None
	return complete_duration
	

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(float(s))

def create_random_selection_for_second_qc(data):
	#retrieve the ones that did not pass
	new_pool=random.sample([element for element in data if element['pass or fail']=='1'],75)
	
	new_pool.extend(random.sample([element for element in data if element['data_pool']!='first'],25))
	

	#prepate the data for the second qc

	keys_needed=['testimony_id','no end','no beginning','comments','other']

	for element in new_pool:
		for key in element.keys():
			if (key not in keys_needed):
				element.pop(key)
		#set the keys to empty:
		element['no end']=''
		element['no beginning']=''
		element['comments']=''
		element['other']=''

		#add element to second qc collection
		testimony_entry=h.query('lts','testimonies',{'testimony_id':element['testimony_id']},{'_id':0})[0]

		#get the pdf
		pdf=h.query(DB,'input_ushmm_metadata',{'irn':element['testimony_id'].split('irn')[1]},{'fnd_doc_filename':1})[0]['fnd_doc_filename']
		testimony_entry['pdf_files']=pdf
		h.insert(DB,'testimonies_for_quality_control',testimony_entry)

		
	text.write_to_csv(new_pool,'second_qc.csv')

if __name__ == '__main__':
	#read the csv file in
	#input_data=text.ReadCSVasDict(input_csv)
	#add_additional_data(input_data)

	#first_round_qc_ed_ids=[element['testimony_id']for element in input_data]
	#all_ids=[element['id'] for element in h.query(DB,constants.USHMM_TRACKER_COLLECTION,{},{'id':1,'_id':0})]
	#not_qc_ed_ids=[{'id':element} for element in all_ids if element not in first_round_qc_ed_ids]
	
	#add_additional_data(not_qc_ed_ids,pool='new')

	input_data=text.ReadCSVasDict('base_data_for_second_qc.csv')
	create_random_selection_for_second_qc(input_data)



	





