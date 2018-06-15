# -*- coding: utf-8 -*-

import json
import os
from pynlpl.formats import folia
import pdb
from nltk.tokenize import sent_tokenize
import pdb
import xml.dom.minidom as xmlprint
import corenlp
import requests
from utils import stanford_parser




def process(folia_doc,prefix):
    """Takes a folia doc string, which is divided into div units, and splits the text of each unit into sentences, adds a unique id to each sentence 
	with a prefix. Returns a new folia doc string which contains also sentence level division. For sentence tokenization it uses NLTK.
    :param folia_doc: folia xml containing division level segmentation
    :param prefix: prefix to be used when adding a unique id to each sentence
    :return: folia xml with division and sentence segmentation
    """

    folia_doc.declare(folia.PosAnnotation,set='brown-tagset')
    folia_doc.declare(folia.LemmaAnnotation,set='treetagger')

    
    #get the first level text
    text=folia_doc.select(folia.Text)
    sentence_id=1
    sentence_index=[1]

    for elements in text:
        for division in elements.select(folia.Division):
            #split each division into sentences
            annotated_division = stanford_parser.annotate(division.text())
            

            #add each sentence to the folia division element

            for sentence in annotated_division['sentences']:
              
		#create a sentence element               
                if len(sentence_index)==1:
                    sentence_element=folia.Sentence(folia_doc,id='s'+str(sentence_index[0]))
                    sentence_index.append(2)

                else: 
                    sentence_element=folia.Sentence(folia_doc,id='s'+str(sentence_index[-1]))
                    sentence_index.append(sentence_index[-1]+1)
                    



                #set the text for the sentence
                
                sentence_element.settext(stanford_parser.sentence_to_text(sentence))
                token_id=1
                for token in sentence['tokens']:

                    #create a token element
                    if not token['after']==' ':

                        token_element=folia.Word(folia_doc,id=sentence_element.id+'_'+str(token_id),space=False)
                    else:
                        token_element=folia.Word(folia_doc,id=sentence_element.id+'_'+str(token_id))

                    token_element.settext(token['originalText'])

                    #annotate it

                    token_element.add(folia.PosAnnotation, set='brown-tagset',cls=token['pos'])
                    token_element.add(folia.LemmaAnnotation, set='treetagger',cls=token['pos'])

                    sentence_element.add(token_element)

                    token_id=token_id+1

                #add the sentence to the division
                division.add(sentence_element)

                


   #Return the result in string
   
    return folia_doc



if __name__ == "__main__":
    
    doc = folia.Document(file=os.getcwd()+'/data/output/sample_folia_divisions.xml',encoding='utf-8')
    result=process(doc,'s')

    #save it

    result.save(os.getcwd()+'/data/output/sample_folia_sentences.xml')










