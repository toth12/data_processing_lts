import pdb	
import os,sys
import glob
import csv
from utils import helper_mongo as h
import codecs
import constants
from utils.text import transform_fields_with_non_latin_characters_to_latin
import codecs
import pandas as pd

##
# Globals
##

# inputs and global config
INPUT_DATA = constants.INPUT_FOLDER_USC_METADATA+'metadata_final_3.csv' # path to metadata xml
db = constants.DB# the database name to use when saving results
OUTPUT_COLLECTION = constants.OUTPUT_COLLECTION_USC


fieldname_map={'IntCode':'testimony_id','IntervieweeName':'interviewee_name','Gender':'gender','Shelfmark':'shelfmark','CollectionOwner':'collection'}


def rename_usc_metadata_fields():
	
	#open the input file and make a python dictionary out of it

	data=pd.read_csv(INPUT_DATA)
	#data['ghetto_names'] = data['ghetto_names'].astype('string')
	data['IntCode'] = data['IntCode'].astype('string')
	data = data.fillna('')
	data = data.to_dict(orient='index')
	data_with_renamed_fields=[]
	for f in data:
		line = data[f]
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
	#load the prepared data
	df_variants = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'ghetto_variants_resolution_sheet.csv')
	df_to_remove = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'ghetto_names_remove_list.csv',header=None)
	df_to_correct = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'ghetto_names_correction_list.csv')
	#result=correction_sheet[correction_sheet.variants.str.contains(text_to_correct)]
	if len(names.strip())>0:
		individual_names=names.strip().split(';')
		for element in individual_names:
			if len(element)>0:
				name=element.split('(')[0].strip()
				#check if it is to be 
				if name in df_to_remove[0].to_list():
					continue
				elif not (df_to_correct[df_to_correct.original_form==name].empty):
					corrected_version = df_to_correct[df_to_correct.original_form==name].final_form.values[0]
					result.append(corrected_version)
				elif not (df_variants[df_variants.variants.str.contains(name)].empty):

					variant_to_include = df_variants[df_variants.variants.str.contains(name)].final_version.values[0]
					result.append(variant_to_include)
				else:
					result.append(name)
	return result

def post_process_camp_names(names):
	result=[]
	#load the prepared data
	df_variants = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'camp_variants_resolution_sheet.csv')
	df_to_remove = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'camp_names_remove_list.csv',header=None)
	df_to_correct = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'camp_names_correction_list.csv')
	#result=correction_sheet[correction_sheet.variants.str.contains(text_to_correct)]

	#if not result.empty:
    #print result.final_version[0]

	if len(names)>0:
		individual_names=names.strip().split(';')
		for element in individual_names:
			if 'Concentration Camp)' in element or 'Death Camp)' in element:
				name=element.split('(')[0].strip()
				if len(name)>2:
					#check if it is to be 
					
					if name in df_to_remove[0].to_list():
						continue
					elif not (df_to_correct[df_to_correct.original_form==name].empty):
						corrected_version = df_to_correct[df_to_correct.original_form==name].final_form.values[0]
						result.append(corrected_version)
					elif not (df_variants[df_variants.variants.str.contains(name)].empty):

						variant_to_include = df_variants[df_variants.variants.str.contains(name)].final_version.values[0]
						result.append(variant_to_include)

					else:
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
		element['shelfmark']= 'USC SHOAH '+element['testimony_id']
		element['testimony_id']='usc_shoah_'+element['testimony_id']
		element['testimony_title']='Oral history interview with '+element['testimony_title']

		if element['gender']=='M':
			element['gender']='male'
		else:
			element['gender']='female'
	return meta_data


def add_youtube_links(data):
	links=pd.read_csv(constants.INPUT_FOLDER_USC_METADATA+"YouTube_links.csv")
	links = links.groupby("IntCode")['YouTubeLink'].apply(list).reset_index(name='media_url')
	data = pd.DataFrame(data)
	data['shelfmark']=pd.to_numeric(data["shelfmark"])
	data = data.drop(columns=['media_url'])
	data = pd.merge(data,links,left_on="shelfmark",right_on="IntCode",how='right')
	return data.T.to_dict().values()
	





def main():
	#create a collection that will hold the data

	os.system('mongo ' + db + ' --eval "db.createCollection(\''+OUTPUT_COLLECTION+'\')"')
	usc_metadata_renamed=rename_usc_metadata_fields()
	usc_metadata_processed=post_process_metadata(usc_metadata_renamed)
	usc_metadata_processed_with_youtube_links = add_youtube_links(usc_metadata_processed)
	

	#usc_metadata_processed=transform_fields_with_non_latin_characters_to_latin(usc_metadata_processed)

	
	#upload result
	h.insert(db,OUTPUT_COLLECTION,usc_metadata_processed_with_youtube_links)

if __name__ == '__main__':
	main()
