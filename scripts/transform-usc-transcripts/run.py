import glob
import pdb	
import os,sys
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
import csv
from parse import transform_transcript_to_structured_unit


##
# Globals
##

db = 'let_them_speak_data_processing'
collection='output_usc_metadata'

def run ():
	'''This function begins the process described in the Readme of this folder'''
	
	#open the transcript list

	reader = csv.DictReader(open('USC_Shoah_Foundation_Transcripts_list.csv', 'rb'))
	
	not_processed=[]
	problematics=['93', '323', '1363', '1511', '1568', '2074', '3022', '3283', '3475', '3858', '3949', '5248', '5388', '5758', '5795', '5970', '7177', '8527', '9024', '9489', '9665', '10010', '10272', '10572', '10587', '11167', '11552', '11611', '12455', '13079', '13213', '13219', '13483', '14212', '14613', '15694', '17299', '17374', '18102', '18960', '19195', '19210', '22685', '22734', '22889', '24814', '25381', '27129', '27759']
	i=1
	for line in reader:
	#get all input filenames
 	#input_files=glob.glob(os.getcwd()+'/inputs/1.*.xml')
 		
 		i=i+1
 		if line['IntCode'] in problematics:
 			print line['IntCode']
	 		#try:
		 	number_of_parts=line['NumTapes']
		 	int_code=line['IntCode']
		 	final_result=[]
		 	for part in range(1,int(number_of_parts)+1):
		 		input_file=os.getcwd()+'/inputs/'+int_code+'.'+str(part)+'.xml'
		 	try:
		 		result=transform_transcript_to_structured_unit(input_file)
		 		final_result.extend(result)
		 			#pdb.set_trace()
		 	except Exception as e: 
				print(e)
		 		not_processed.append(line['IntCode'])
	pdb.set_trace()
 	
	#get the shelfmarks of the input files
	shelf_marks=list(set([element.split('/')[-1].split('.')[0]for element in input_files]))
	'''
	#create the output collection
	os.system('mongo ' + db + ' --eval "db.createCollection(\''+collection+'\')"')

	testimony_ids = [{'testimony_id': value} for value in shelf_marks]	#upload shelfmarks

	h.insert(db,collection,testimony_ids)
	#pdb.set_trace()

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
	for element in shelf_marks_with_filenames:

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
	
	for shelfmark in shelf_marks_with_filenames:
		
		#create a list that will store the result of segmentation
		result=[]

		#use a try catch block to store the shelfmarks that could not be processed
		try:
			for files in shelf_marks_with_filenames[shelfmark]:
			
				#process the transcript by passing the filename to the segment_transcript function
				result.extend(segment_transcript(files))
			
			
			final_result.append({shelfmark:result})
			
		except:
			#in case the processing was not possible store the shelfmark
			unprocessed.append(shelfmark)

		
	#print those shelfmarks that could not be processed
	print unprocessed

	#check if there are shelfmarks that are missing from the dataset
	missing=[int(element.split('_')[1]) for element in shelf_marks_with_filenames.keys()]
	missing.sort()
	missing_shelfmarks=[]
	
	for element in range(1,184):
		
		if element not in missing:
			missing_shelfmarks.append(element)

	#upload the results to the DB

	for element in final_result:

		#get the unique id of the entry based on the shelfmark
		entry_id=h.query(db,collection,{'testimony_id':element.keys()[0]},{})[0]
		h.update_entry(db,collection,entry_id['_id'],{'structured_transcript':element[element.keys()[0]]})

	#delete those entries that could not be processed
	
	
	#db.output_fortunoff_metadata.remove( {'structured_transcript': { $exists: false } } )
	#os.system('mongo ' + db + ' --eval "db.output_fortunoff_metadata.remove({\'structured_transcript\': { $exists: false } } )"')
	
	h.delete(db,collection,{'structured_transcript': { '$exists': False } })

	pdb.set_trace()


	'''
				





if __name__ == '__main__':
	run()