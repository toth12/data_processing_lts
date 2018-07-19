import sys, os
import pdb
#set utils path
helper_path = os.getcwd()+"/utils"
sys.path.insert(0, helper_path)
import helper_mongo as h


ids=h.query('lts', 'testimonies',{},{'testimony_id':1})

ids_without_ushmm=[element['testimony_id'] for element in ids if element['testimony_id'][0]!='i']

for e in ids_without_ushmm:
	doc=h.query('lts', 'testimonies',{'testimony_id':e},{'html_transcript':1})[0]
	
	h.update_field('let_them_speak_data_processing_test','testimonies','testimony_id',e,'html_transcript', doc['html_transcript'])
	
