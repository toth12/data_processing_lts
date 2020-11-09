from parse import segment_transcript
import glob
import pdb	
import os,sys
import helper_mongo as h
import constants
import pandas as pd


##
# Globals
##

db = constants.DB
collection=constants.OUTPUT_COLLECTION_FORTUNOFF
input_folder=constants.INPUT_FOLDER_FORTUNOFF_TRANSCRIPTS
OUTPUT_FOLDER_FORTUNOFF_PROCESSING_LOGS=constants.OUTPUT_FOLDER_FORTUNOFF_PROCESSING_LOGS

def run (debug):
	'''This function begins the process described in the Readme of this folder'''
	
	#get all input filenames
 	input_files=glob.glob(input_folder+'*.txt')
	#get the shelfmarks of the input files
	shelf_marks=list(set(['_'.join(element.split('/')[-1].split('_')[1:3])for element in input_files]))

	testimony_ids = [{'testimony_id': value} for value in shelf_marks]	#upload shelfmarks

	#read the surnames of survivors
	names=pd.read_csv(constants.INPUT_FOLDER_FORTUNOFF_METADATA+'Fortunoff_first_names.csv' )
	names['surname']=names.primary_name.apply(lambda x: x.split(',')[0].strip())
	


	#find the corresponding transcript files of each shelfmark
	#create a dictionary with shelfmarks as keys, and values as empty dictionary
	shelf_marks_with_filenames={}


	for element in shelf_marks:
		shelf_marks_with_filenames[element]=[]

	for element in input_files:
		
		#find the shelfmark of each file
		shelf='_'.join(element.split('/')[-1].split('_')[1:3])
		
		#add the file name to dictionary with shelfmarks as keys
		shelf_marks_with_filenames[shelf].append(element)


	#the dictionary with shelfmarks contains all shelfmarks with corresponding filenames but not necessarily in the right order, this part of the script reorders them
	for c,element in enumerate(shelf_marks_with_filenames):
		
		#set the debug to here
		if (debug == True) and (c==10):
			break


		#create an empty list that will hold the ordered list of transcript parts
		ordered_list=[]

		#get the number of transcript parts
		number_of_parts=int(str(shelf_marks_with_filenames[element][0].split('_p')[1].split('.')[0].split('of')[1]))


		#iterate through the number of parts
		for i in range(1,number_of_parts+1):
	
			#find the transcript corresponding to a given part
			for x in shelf_marks_with_filenames[element]:
				
				#get the part number from the filename
				part=int(x.split('_p')[1].split('.')[0].split('of')[0])
				
				#check if the part corresponds to the order defined in the range above
				if part ==i:
					#add it to the ordered list in case yes
					ordered_list.append(x)

		#replace the reordered list with the not ordered list
		shelf_marks_with_filenames[element]=ordered_list
	
	#process files belonging to each shelfmark and join them
	#create an empty dictionary to store the shelfmarks that could not be processed
	unprocessed=[]
	final_result=[]
	
	for c, shelfmark in enumerate(shelf_marks_with_filenames):

		#set the debug to here
		if (debug == True) and (c==10):
			break
		
		#create a list that will store the result of segmentation
		result=[]
		#use a try catch block to store the shelfmarks that could not be processed
		try:
			for i,files in enumerate(shelf_marks_with_filenames[shelfmark]):
				


				#find the relevant surname
				surnames = names[names.Identifier==shelfmark.upper().replace('_','-')]['surname'].values

				#process the transcript by passing the filename to the segment_transcript function
				processed_transcript=segment_transcript(files,shelfmark,surnames)
				
				#add a change of tape message
				if i!=0:
					result.extend([{'unit':'Change of tape'}])
				result.extend(processed_transcript)
			
			
			final_result.append({shelfmark.upper().replace('_','-'):result})
			
		except Exception as e:
			#in case the processing was not possible store the shelfmark
			unprocessed.append(shelfmark)

		
	#check if there are shelfmarks that are missing from the dataset
	missing=[int(element.split('_')[1]) for element in shelf_marks_with_filenames.keys()]
	missing.sort()
	missing_shelfmarks=[]
	
	for element in range(1,184):
		
		if element not in missing:
			missing_shelfmarks.append('HVT-'+str(element))

	#upload the results to the DB

	for element in final_result:
		#get the unique id of the entry based on the shelfmark
		entry_id=h.query(db,collection,{'testimony_id':element.keys()[0]},{})[0]

		h.update_entry(db,collection,entry_id['_id'],{'structured_transcript':element[element.keys()[0]]})

	#delete those entries that could not be processed
	#h.delete(db,collection,{'structured_transcript': { '$exists': False } })


	print ("The processing of the following shelfmarks was not possible, they are logged into: "+OUTPUT_FOLDER_FORTUNOFF_PROCESSING_LOGS)

	print('\n'.join(unprocessed))
	#write the missing files to text file
	file = open(OUTPUT_FOLDER_FORTUNOFF_PROCESSING_LOGS+'processing_failed.txt','w')
	file.write('\n'.join(unprocessed))
	
	print ("The following shelfmark was missing, it is logged into: "+OUTPUT_FOLDER_FORTUNOFF_PROCESSING_LOGS)
	
	print('\n'.join(missing_shelfmarks))

	#write the missing files to text file
	file = open(OUTPUT_FOLDER_FORTUNOFF_PROCESSING_LOGS+'missing_shelfmark.txt','w')
	file.write('\n'.join(missing_shelfmarks))
				
	




if __name__ == '__main__':
	run()