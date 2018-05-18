import json
import os
from pynlpl.formats import folia
import pdb
from nltk.tokenize import sent_tokenize
import pdb
import xml.dom.minidom as xmlprint



def process(folia_doc,prefix):
    """Takes a folia doc string, which is divided into div units, and splits the text of each unit into sentences, adds a unique id to each sentence 
	with a prefix. Returns a new folia doc string which contains also sentence level division. For sentence tokenization it uses NLTK.
    :param folia_doc: folia xml containing division level segmentation
    :param prefix: prefix to be used when adding a unique id to each sentence
    :return: folia xml with division and sentence segmentation
    """


    
    #get the first level text
    text=folia_doc.select(folia.Text)
    sentence_id=1
    for elements in text:
        for division in elements.select(folia.Division):
            #split each division into sentences
            sent_tokenize_list = sent_tokenize(division.text())

            #add each sentence to the folia division element

            for sentence in sent_tokenize_list:
              
		#create a sentence element               
               
                sentence_element=folia.Sentence(folia_doc,id='s'+str(sentence_id)) 
                #set the text for the sentence
                
                sentence_element.settext(sentence)

                #add the sentence to the division

                division.add(sentence_element)

                sentence_id=sentence_id+1


   #Return the result in string
   
    return folia_doc

if __name__ == "__main__":
    #read sample input
    doc = folia.Document(file=os.getcwd()+'/data/output/sample_folia_divisions.xml')
    result=process(doc,'s')

    #save it

    result.save(os.getcwd()+'/data/output/sample_folia_sentences.xml')








