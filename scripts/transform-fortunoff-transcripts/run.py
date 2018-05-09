from parse import segment_transcript
import glob
import pdb	
import os

def run ():
	'''This function begins the process described in the Readme of this folder'''
	
	#get all input filenames
 	input_files=glob.glob(os.getcwd()+'/inputs/*.txt')

	#get the shelfmarks of the input files
	shelf_marks=list(set(['_'.join(element.split('/')[-1].split('_')[1:3])for element in input_files]))
	
	

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
			final_result.append(result)
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

	pdb.set_trace()
				





if __name__ == '__main__':
	run()