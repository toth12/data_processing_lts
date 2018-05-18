import json
import os
from pynlpl.formats import folia
import pdb
from nltk.tokenize import word_tokenize
import xml.dom.minidom as xmlprint
from bs4 import BeautifulSoup
import sys
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h

def process(folia_doc,testimony_id):
    """Takes a folia xml, which is divided into div, sentence and token units, and creates a token sentence id look up dictionary. The position of token in the entire document is the dictionary key, the assigned value is the
    is the unique id of the sentence in which it occur.

    :param folia_doc_string: folia xml containing division, sentence and token level segmentation
    :return: look up dictionary"""
    #get each tokens

    tokens=folia_doc.select(folia.Word)
    #build up the look up dictionary by getting the sentence id as well
    
    look_up_index = [{'token_index': index,'sentence_index':int(token.parent.id[1:])} for index,token in enumerate(tokens)]
    look_up_table={"testimony_id":testimony_id,'tokens':look_up_index}
    #an alternative way to do thislook_up_table=[token.parent.id for token in tokens]
    
    return look_up_table


if __name__ == "__main__":
    #read sample input
    doc = folia.Document(file=os.getcwd()+'/data/output/sample_folia_pos_tagged.xml')
    #todo: decide what the input should be for this function
    result=process(doc,'some_id')
 







