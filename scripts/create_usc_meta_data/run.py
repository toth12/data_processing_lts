import pdb	
import os,sys
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import glob
import csv
import helper_mongo as h
import codecs


##
# Globals
##

db = 'let_them_speak_data_processing'
collection='output_usc_metadata'

fieldname_map={'IntCode':'testimony_id','IntervieweeName':'interviewee_name','Gender':'gender','Shelfmark':'shelfmark','CollectionOwner':'collection'}


input_file=os.getcwd()+'/input/transcript_testimonies_info_for_Gabor.csv'



def rename_usc_metadata_fields():
	
	#open the input file and make a python dictionary out of it

	reader = csv.DictReader(open(input_file, 'rb'))
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
		new_entry['recording_year']=None
		data_with_renamed_fields.append(new_entry)
	
	return data_with_renamed_fields

def post_process_ghetto_camp_names(names):
	result=[]
	if len(names)>0:
		individual_names=names.strip().split(';')
		for element in individual_names:
			if len(element)>0:
				name=element.split('(')[0].strip().decode('utf-8',errors='replace')
				result.append(name)
	return result




def post_process_metadata(meta_data):

	for element in meta_data:
		#postprocess ghetto names
		element['ghetto_names']=post_process_ghetto_camp_names(element['ghetto_names'])
		element['camp_names']=post_process_ghetto_camp_names(element['camp_names'])

		#provenance to be left empty
		element['provenance']=''
		element['interviewee_name']=element['interviewee_name'].decode('utf-8',errors='replace')
		element['shelfmark']='USC Shoah '+element['testimony_id']
		element['testimony_id']='usc_shoah_'+element['testimony_id']
		element['testimony_title']='Oral history interview with '+element['testimony_title'].decode('utf-8',errors='replace')

		if element['gender']=='m':
			element['gender']='male'
		else:
			element['gender']='female'
	return meta_data








if __name__ == '__main__':
	#create a collection that will hold the data

	os.system('mongo ' + db + ' --eval "db.createCollection(\''+collection+'\')"')

	usc_metadata_renamed=rename_usc_metadata_fields()
	usc_metadata_processed=post_process_metadata(usc_metadata_renamed)

	#upload result
	h.insert(db,collection,usc_metadata_processed)
	pdb.set_trace()