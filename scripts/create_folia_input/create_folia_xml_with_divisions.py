import json
import os
from pynlpl.formats import folia
import pdb

def process(units,testimony_id,shelf_mark,year,ghetto,camp,gender):
    """Takes a python list consisting of dictionaries with units, and transforms into a folia xml file consisting of divisions
    :param untis: list of dictionaries with key unit
    :param doc_id: unique id to be given to the folia doc
    :return: folia xml
    """

    #todo: add metadata to here


    #create a new folia document
    new_doc=folia.Document(id=testimony_id)
    new_doc.metadata['shelfmark']='USHMM-'+shelf_mark
    new_doc.metadata['testimony_id']=testimony_id
    new_doc.metadata['ghetto']=ghetto
    new_doc.metadata['camp']=camp
    new_doc.metadata['gender']=gender
    text=folia.Text(new_doc)
    #iterate through the input to create the folia division elements

    for unit in units:
        division=folia.Division(new_doc)
        division.settext(unit['unit'])
        text.add(division)
    new_doc.add(text)
    return new_doc


if __name__ == "__main__":
    #read sample input
    with open(os.getcwd()+'/data/input/sample_input.json') as json_data:
        sample_data = json.load(json_data) 
    result=process(sample_data,'some_id','some_shelf_mark')
    #save result with folia tool

    result.save(os.getcwd()+'/data/output/sample_folia_divisions.xml')









