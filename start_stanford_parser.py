import sys, os
import pdb
#set utils path
helper_path = os.getcwd()+"/utils"
sys.path.insert(0, helper_path)
import stanford_parser
import constants

if __name__ == '__main__':
	stanford_parser.start_stanfordcornlp_server(constants.CORENLP_HOME)