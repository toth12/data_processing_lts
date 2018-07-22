#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Text data helpers
'''

import json
import codecs
import regex as re
import unidecode
from six import string_types
import pdb
import csv


def read(path, codec):
  '''
  Read a file with a given codec
  @args:
    {str} path: the path to the file to read
    {str} codec: the encoding to use while reading
  @returns:
    {str} the read file
  '''
  with codecs.open(path, 'r', codec) as f:
    return f.read()

def get_tag(s, tag, loud=True):
  '''
  Get the content between `<tag>` and `</tag>` in `s`
  @args:
    {str} s: an input string with markup
    {str} tag: the tag whose internal content should be fetched
  @returns:
    {str} a string with the content between `<tag>` and `</tag>`
  '''
  try:
    return s.split('<' + tag + '>')[1].split('</' + tag + '>')[0]
  except IndexError:
    if loud: print(' ! tag parse failed', tag)
    return ''

def get_attr(s, attr):
  '''
  Get the attribute content of `attr` within `s`
  @args:
    {str} s: an input string with markup
    {str} attr: the attribute whose value will be returned
  @returns:
    {str} the inner content of `attr`
  '''
  return s.split(attr + '="')[1].split('"')[0]

def get_year(s):
  '''
  Return the first four consecutive integers from a string
  @args:
    {str} s: a string that should contain a four digit year
  @returns:
    {str} the first four-digit number in `s`
  '''
  integers = [str(i) for i in range(10)]
  for hyphen_component in s.split('-'):
    for square_component in hyphen_component.split('['):
      for slash_component in square_component.split('/'):
        for token in slash_component.split(' '):
          clean_token = ''
          for character in token:
            if character in integers:
              clean_token += character
          if len(clean_token) == 4:
            return clean_token
  print(' ! year parse failed', s)
  return s

def strip_punctuation(s):
  '''
  Remove puncutation from a string
  @args:
    {str} s: a string
  @returns:
    {str} `s` stripped of punctuation
  '''
  return re.sub(r'[^\P{P}-]+', '', s)

def escape_quotes(s):
  '''
  Unicode escape quotes in `s`
  @args:
    {str} s: a string
  @returns:
    {str} `s` with quote characters unicod escaped
  '''
  s = s.replace('"', '\u0022') # double quote
  s = s.replace("'", '\u0027') # single quote
  s = s.replace('`', '\u0060') # grave
  s = s.replace('‘', '\u2018') # left single quote
  s = s.replace('’', '\u2019') # right single quote
  s = s.replace('“', '\u201C') # left double quote
  s = s.replace('”', '\u201D') # right double quote
  return s

def read_json(path):
  '''
  Read in the JSON at `path`
  @args:
    {str} path: the path to a JSON file
  @returns:
    {obj} a JSON object
  '''
  with open(path) as f:
    return json.load(f)


def write_json(path, obj):
  '''
  Write JSON to disk
  @args:
    {str} path: the path where `obj` will be written
    {obj} obj: a JSON object
  '''
  with open(path, 'w') as out:
    json.dump(obj, out)


def get_stopwords():
  '''
  Return a set of stopwords
  '''
  with codecs.open('utils/data/stopwords.txt', 'r', 'utf8') as f:
    return set(f.read().split())

def transform_fields_with_non_latin_characters_to_latin(records):
  '''
  Takes a python list of dictionaries and transliterates all values in the dictionary
  @args:
    {list} records: python list of dictionaries
  @returns:
    {dict} same dictionary with transliterated fields
  '''
  
  for i,elements in enumerate(records):
    
    for element in elements:
      if type(elements[element]) is list:
        for f,d in enumerate(elements[element]):

          records[i][element][f]=unidecode.unidecode(d)
          
      else:
        if not ((type(records[i][element]) is int) or (records[i][element] is None)):
          try:
            records[i][element]=unidecode.unidecode(records[i][element])
          except:
            pdb.set_trace()
  return records

def ReadCSVasDict(csv_file):
    result=[]
    try:
        with open(csv_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result.append(row)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))    
    return result

if __name__ == "__main__":
  records=[{'ghetto_names':['Łódź'],'recording_year':1999,'camp_names':[],'name':''}]
  expected_output=[{'ghetto_names':['Lodz'],'recording_year':1999,'camp_names':[],'name':''}]
  print (transform_fields_with_non_latin_characters_to_latin(records))
