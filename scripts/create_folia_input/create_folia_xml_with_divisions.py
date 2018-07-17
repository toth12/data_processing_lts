import json
import os
from pynlpl.formats import folia
import pdb

def process(data):
    """Takes a python list consisting of dictionaries with units, and transforms into a folia xml file consisting of divisions
    :param untis: list of dictionaries with key unit
    :param doc_id: unique id to be given to the folia doc
    :return: folia xml
    """

    #todo: add metadata to here


    #create a new folia document
    new_doc=folia.Document(id=data['testimony_id'])
    new_doc.metadata['shelfmark']=data['shelfmark']
    new_doc.metadata['testimony_id']=data['testimony_id']
    new_doc.metadata['ghetto_names']=' '.join(data['ghetto_names'])
    new_doc.metadata['camp_names']=' '.join(data['camp_names'])
    new_doc.metadata['gender']=data['gender']
    new_doc.metadata['collection']=data['collection']
    new_doc.metadata['interviewee_name']=data['interviewee_name']
    new_doc.metadata['recording_year']=data['recording_year']


    text=folia.Text(new_doc)
    #iterate through the input to create the folia division elements

    for unit in data['structured_transcript']:
        pdb.set_trace()
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









