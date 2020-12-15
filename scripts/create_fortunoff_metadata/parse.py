'''
Transform the Marc XML from UC Riverside to JSON and save in Mongo
'''

from text import read,transform_fields_with_non_latin_characters_to_latin
from api import save, config
from marc import get_marc_fields
from collections import defaultdict, Counter
from glob import glob
import codecs
import os
import xmltodict
import sys
import json
import constants
import pdb
import helper_mongo as h
import pandas as pd

##
# Globals
##



# inputs and global config
INPUT_DATA='fortunoff-marc.xml'
marc_xml_path = constants.INPUT_FOLDER_FORTUNOFF_METADATA+'fortunoff-marc.xml' # path to metadata xml
db = constants.DB# the database name to use when saving results
OUTPUT_COLLECTION = constants.OUTPUT_COLLECTION_FORTUNOFF
max_records = 182 # max records to process (int|None)
#complete number of records: 4390


# marc fields to process
fields = [
  {
    'number': '245',
    'letter': 'a',
    'label': 'testimony_title',
  },
  
  {
    'number': '100',
    'letter': 'a',
    'label': 'interviewee_name',
  },
  {
    'number': '520',
    'letter': 'a',
    'label': 'interview_summary',
  },
  {
    'number': '610',
    'letter': 'a',
    'label': 'camp_names_1',
    'type': list
  },
  {
    'number': '690',
    'letter': 'a',
    'label': 'camp_names_2',
    'type': list
  },
  {
    'number': '691',
    'letter': 'a',
    'label': 'camp_names_3',
    'type': list
  },
  {
    'number': '691',
    'letter': 'a',
    'label': 'ghetto_names',
    'type': list
  },
  {
    'number': '090',
    'letter': 'b',
    'label': 'testimony_id',
  },
  {
    'number': '260',
    'letter': 'b',
    'label': 'provenance',
  },
  {
    'number': '260',
    'letter': 'c',
    'label': 'recording_year',
  },
  {
    'number': '650',
    'letter': '0',
    'label': 'gender',
  }
]

##
# Testimony Metadata Functions
##

def get_marc_json():
  '''
  Parse MarcXML from UC Riverside and return a list
  of JSON records from that XML file
  '''
  records = []
  # marcxml was delivered from UC Riverside
  f = read(marc_xml_path, 'utf8')
  for idx, i in enumerate(f.split('<marc:record>')[1:]):
    if max_records and idx > max_records:
      continue
    xml = '<record>' + i.split('</marc:record>')[0] + '</record>'
    records.append(xmltodict.parse(xml))
 
  return records


def get_field(d):
  '''
  Given a dict `d`, find the MARC code within that
  d and return that code and its value
  @args:
    {obj} d: an object with MARC XML
  @returns:
    {obj} an object with the code and value from d
  '''
  if '@code' in list(d.keys()) and '#text' in list(d.keys()):
    return {
      'code': d['@code'],
      'text': d['#text'],
    }
  return None


def nest_marc_json(arr):
  '''
  Format the JSON parsed from MarcXML
  @args:
    {arr} arr: a list of json records
  @returns:
    {arr} a formatted list of json records
  '''
  records = []
  for idx, i in enumerate(arr):
    record_json = defaultdict(lambda: defaultdict(list))
    record = i['record']

    # 001 = estc_id, 009 = estc internal id
    for j in record['marc:controlfield']:
      tag = j['@tag']
      if tag in ['001', '009']:
        record_json[tag] = j['#text']

    # get record metadata from datafields
    for c, j in enumerate(record['marc:datafield']):
      tag = record['marc:datafield'][c]['@tag']
      if 'marc:subfield' in list(record['marc:datafield'][c].keys()):
        subfield = record['marc:datafield'][c]['marc:subfield']

        # some subfields are arrays of objects, others are objects
        if not isinstance(subfield, list):
          subfield = [subfield]

        for subfield_dict in subfield:
          field = get_field(subfield_dict)
          if field:
            record_json[tag][field['code']].append(field['text'])
          else:
            pass

    parsed = to_dict(record_json)
    records.append(parsed)
  return records


def to_dict(d):
  '''
  Convert a nested defaultdict to a dictionary
  @args:
    {defaultdict} d: a nested defaultdict
  @returns:
    {dict} a plain nested dictionary
  '''
  if isinstance(d, defaultdict):
    d = {k: to_dict(v) for k, v in d.items()}
  return d


def flatten_marc_json(records):
  '''
  Convert a list of documents in nested Marc JSON to
  a list of documents in flat JSON with app-specific
  keys
  '''
  parsed_records = []
  for i, record in enumerate(records):
    
    parsed = get_marc_fields(record, fields)
    parsed['gender'] = clean_gender(parsed['gender'])
    parsed['collection'] = 'Fortunoff'
    parsed['shelfmark'] = 'Fortunoff '+parsed['testimony_id']
    parsed['recording_year'] = clean_year(parsed['recording_year'])
    parsed['media_url'] = []
    parsed['thumbnail_url'] = ''
    parsed['camp_names']=parsed['camp_names_1']+parsed['camp_names_2']+parsed['camp_names_2']
    parsed['camp_names'] = clean_camp_names(parsed['camp_names_1'])
    parsed['provenance'] = clean_provenance(parsed['provenance'])
    parsed['ghetto_names']=clean_ghetto_names(parsed['ghetto_names'])
    
    #delete unnecessary fields
    parsed.pop('camp_names_1',None)
    parsed.pop('camp_names_2',None)
    parsed.pop('camp_names_3',None)
    

    # check if double interview and then eliminate the gender info

    if 'and' in parsed['testimony_title'].split():
      parsed['gender'] = ''
    # add the parsed record to the list of parsed records
    parsed_records.append(parsed)
  return parsed_records


def clean_gender(gender):
  '''
  @args:
    {arr} gender: a list of urls, one them is the gender attribute of interviews
  @returns:
    {arr} 'M' or 'F' or 
  '''

  #check if multiple gender info is present, in this case this is a couple

  gender_urls={'F':'http://id.loc.gov/authorities/subjects/sh85147274','M':'http://id.loc.gov/authorities/subjects/sh85083510'}
  
  if (gender_urls['F'] in gender) and (gender_urls['M'] in gender):
    gender =''
  elif (gender_urls['F'] in gender):
    gender='female'
  elif (gender_urls['M'] in gender):
    gender = 'male'
  else:
    gender =''
   
  return gender

def clean_year(recording_year):
  '''
  @args:
    {arr} recording_year: a string representing the year when the interview was recorded
  @returns:
    {arr} string representation of the year without the dot at the end
  '''
  
  return int(recording_year[0:4])

def clean_camp_names(camp_names):
  '''
  @args:
    {arr} camp_names: a list of strings
  @returns:
    {arr} a list of strings
  '''

  if len(camp_names)>0:
    result=[]
    for element in camp_names:
      if '(Concentration camp)' in element:
        result.append(element.split('(Concentration camp)')[0].strip())
    return result
  else:
    return camp_names


def clean_provenance(provenance):
  '''
  @args:
    {str} provenance: a string reflecting the provenance of a record
  @returns:
    {str}: a string
  '''
  return provenance.strip().rstrip(',')


def clean_ghetto_names(ghetto_names):
  '''
  @args:
    {str} provenance: a string reflecting the provenance of a record
  @returns:
    {str}: a string
  '''
  
  if len(ghetto_names)>0:
    result=[]
    for element in ghetto_names:
      if 'ghetto' in element:
        
        result.append(element.split('ghetto.')[0].strip())
    return result
  else:
    return ghetto_names

def format_marc():
  '''
  Return a list of dictionaries, where each dict represents a
  testimony and possesses the required keys
  '''
  marc_json = get_marc_json()

  marc_json_nested = nest_marc_json(marc_json)
  #ez kell
  marc_json_flat = flatten_marc_json(marc_json_nested)
  
  return marc_json_flat



def harmonize_camp_names(field):

    OUTPUT_COLLECTION = constants.OUTPUT_COLLECTION_FORTUNOFF
    DB = constants.DB
    names = h.query(DB, OUTPUT_COLLECTION, {}, {field: 1,'id':1} )

    #load the prepared data
    if field =="camp_names":

        df_variants = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'camp_variants_resolution_sheet.csv')
        df_to_remove = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'camp_names_remove_list.csv',header=None)
        df_to_correct = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'camp_names_correction_list.csv',encoding='utf-8')
    
    elif (field=="ghetto_names"):
        df_variants = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'ghetto_variants_resolution_sheet.csv')
        df_to_remove = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'ghetto_names_remove_list.csv',header=None)
        df_to_correct = pd.read_csv(constants.METADATA_CORRECTION_DOCS+'ghetto_names_correction_list.csv',encoding='utf-8')
    


    try:
        for entry in names:
            if len(entry[field])==0:
                continue
            else:
                result=[]
                for name in entry[field]:
                    if name == '\xc5\x81\xc3\xb3d\xc5\xba':
                        pdb.set_trace()
                    if name =='Block 10 (Auschwitz':
                        name = 'Auschwitz'

                    elif name in df_to_remove[0].to_list():
                        continue
                    elif not (df_to_correct[df_to_correct.original_form==name.encode('utf-8').strip()].empty):
                        corrected_version = df_to_correct[df_to_correct.original_form==name.encode("utf-8").strip()].final_form.values[0]
                        result.append(corrected_version)
                    elif not (df_variants[df_variants.variants.str.contains(name.encode('utf-8').strip())].empty):

                        variant_to_include = df_variants[df_variants.variants.str.contains(name.encode("utf-8").strip())].final_version.values[0]
                        result.append(variant_to_include)

                    else:
                        result.append(name.encode('utf-8').strip())
                
                h.update_field(DB,OUTPUT_COLLECTION, '_id', entry['_id'], field, result)
            
    except:
        pdb.set_trace()
    


##
# Main
##

def main():

  

  # process records
  records = format_marc()
  #records=transform_fields_with_non_latin_characters_to_latin(records)

  
  #save it to the DB
  save(records, OUTPUT_COLLECTION)
  harmonize_camp_names(field="camp_names")
  harmonize_camp_names(field="ghetto_names")




  