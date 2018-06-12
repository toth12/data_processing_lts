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

def add_pdf_files():
 

 results=h.query(output_db, 'testimonies_for_quality_control', {},{'_id':1,'testimony_id':1})
 for result in results:
 		#check if already in the testimonies collection
 		pdf=h.query(input_db,'input_ushmm_metadata',{'irn':result['testimony_id'].split('irn')[1]},{'fnd_doc_filename':1})[0]['fnd_doc_filename']
 		
 		h.update_entry(output_db,'testimonies_for_quality_control',result['_id'],{'pdf_files':pdf})

 

def create_csv_file():
	entries=[]
	results=h.query(output_db, 'testimonies_for_quality_control', {},{'_id':1,'testimony_id':1})
	for result in results:
		entry={'testimony_id':' ','pass or fail':' ','no beginning':' ','no end':' ','not segment and not monologue':'','presence of odd words':'','monologue':'','time stamps in the file':'','only answers and not monologue':'','only questions':' ','other':' ','comments':''}

		entry['testimony_id']=result['testimony_id']
		entries.append(entry)
	
	WriteDictToCSV(output_folder+'quality_control.csv',entry.keys(),entries)




if __name__ == '__main__':

	#duplicate the testimonies db 

	os.system('mongo ' + output_db + ' --eval "db.testimonies.find({\'collection\':\'USHMM\',\'status\':\'transcript_processed\'}).forEach(function(doc){db.testimonies_for_quality_control.insert(doc);});"')

	
	#db.testimonies.find({'collection':'USHMM','status':'transcript_processed'}).forEach(function(doc){db.testimonies_for_quality_control.insert(doc);});
	
	add_pdf_files()

	create_csv_file()

	#dump the collection

	os.system('mongodump --db=' + output_db + '--collection=testimonies_for_quality_control --archive='+output_folder+'testimonies_for_quality_control.archive')

	#delete the collection

	os.system('mongo ' + output_db + ' --eval "db.testimonies_for_quality_control.drop()')
