import os
import csv
import pdb
import codecs
import pandas
import math

####Globals####

input_fragment_gt=os.getcwd()+"/data/inputs/fragments/fragments_by_gt.csv"
input_fragment_ec=os.getcwd()+"/data/inputs/fragments/fragments_by_ec.csv"


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
			
	pdb.set_trace()
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


if __name__ == '__main__':
	fragments_gt=read_csv(input_fragment_gt)
	fragments_ec=read_csv(input_fragment_ec)
	result=update_fragments(fragments_gt,fragments_ec)


	WriteDictToCSV('fragments.csv',result[0].keys(),result)

