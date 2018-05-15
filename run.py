import sys, os
import pdb
helper_path = os.getcwd()+"/utils"
sys.path.insert(0, helper_path)
pdb.set_trace()

from scripts.create_ushmm_metadata import run as create_ushmm_metadata




def process_data():

 #transform USHMM catalogue data to app specific metadata
 create_ushmm_metadata.main()

if __name__ == '__main__':
	
	process_data()