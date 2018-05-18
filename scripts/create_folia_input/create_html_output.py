import json
import os
from pynlpl.formats import folia
import pdb
from nltk.tokenize import word_tokenize
import xml.dom.minidom as xmlprint
from bs4 import BeautifulSoup


def process(folia_doc):
    """Takes a folia doc string, which is divided into div, sentence and token units, and exports it into html. The result html doc is divided into 
	paragraphs according to the divisions in the input folia doc, and into sentences with span elements. Each sentence has a unique id taken from the folia input.

        :param folia_doc_string: folia xml in srtring format containing division, sentence and token level segmentation
        :return: html string with each division in the folia input transformed to p element, and each sentence transformed to span element with a unique id"""


    #get each division 
    divisions=folia_doc.select(folia.Division)
    division_texts=[]
    for division in divisions:
        #get the sentences of each division
        sentences=division.select(folia.Sentence)
        sentence_texts=[]
        for sentence in sentences:
            sentence_texts.append('<span id="'+sentence.id+'">'+sentence.text()+'</span>')
        division_texts.append('<p>'+' '.join(sentence_texts)+'</p>')
    html=BeautifulSoup(' '.join(division_texts),'lxml')

    return str(html)


if __name__ == "__main__":
    #read sample input
    doc = folia.Document(file=os.getcwd()+'/data/output/sample_folia_pos_tagged.xml')

    result=process(doc)

    #save it

    with open(os.getcwd()+"/data/output/sample_html_output.html", "w") as file:
            file.write(result)







