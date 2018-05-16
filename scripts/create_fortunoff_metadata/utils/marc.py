#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Helpers for processing Marc XML and JSON
'''
import pdb
def get_marc_fields(record, fields):
  '''
  Get a list of fields from a Marc record
  @args:
    record: a Fortunoff Marc record
    fields: {arr}
      number: {str} a number (as str) for a Marc field
      numbers: {arr} a list of numbers (as str) for a Marc field
      letter: {str} a letter for a Marc field
      label: {str} a human-readable label for a Marc field
      type: {list} if list, return a list of responses
  @returns:
    {obj} an object with one `label` per field as a top-level
      key, with the value of that key representing the value
      of the given field in the Marc record
  '''
  result = {}
  
  for field in fields:
    args = get_field_args(field)
    label = args['label']
    

    # some marc fields have list values, e.g. 655a
    if args['field_type'] == list or label=='gender':
      result[label] = get_list_field(record, args)
      # most marc fields have string values
    else:
      result[label] = get_str_field(record, args)

  return result


def get_field_args(field):
  '''
  Return the arguments to be used when parsing a Marc field
  @args:
    {obj} field: an object that defines the Marc field to parse
      number: the Marc field number to parse (if any)
      numbers: the Marc field numbers to parse (if any)
      letter: the Marc field letter to parse (if any)
      field_type: the type of object to be stored for this Marc
        field (e.g. str, list)
  @returns:
    {obj} field: an object that defines the Marc field to parse
      number: the Marc field number to parse (if any)
      numbers: the Marc field numbers to parse (if any)
      letter: the Marc field letter to parse (if any)
      field_type: the type of object to be stored for this Marc
        field (e.g. str, list)
  '''
  return {
    'number': field.get('number', None),
    'numbers': field.get('numbers', None),
    'letter': field.get('letter', None),
    'label': field.get('label', None),
    'field_type': field.get('type', str),
  }


def get_list_field(record, args):
  '''
  Return the Marc field defined by `args` within `record`
  @args:
    {obj} record: an object that defines the Marc field to parse
      number: the Marc field number to parse (if any)
      numbers: the Marc field numbers to parse (if any)
      letter: the Marc field letter to parse (if any)
      field_type: the type of object to be stored for this Marc
        field (e.g. str, list)
  @returns:
    {arr} a list with the content of the requested Marc field
  '''
  l = []
  number = args['number']
  letter = args['letter']

  # some marc fields use an integer range, e.g. subjects = 600-699
  if args['numbers']:
    for number in args['numbers']:
      for letter in record.get(number, {}):
        for val in record.get(number, {}).get(letter, []):
          l.append(val)

  # marc fields with a single number field
  else:

    # some requests need lists for a letter
    if letter:
      for val in record.get(number, {}).get(letter, []):
        l.append(val)

    # others need lists for all letters in a number
    else:
      for letter in record.get(number, {}):
        for val in record.get(number, {}).get(letter, []):
          l.append(val)

  # dedupe list results while preserving order
  deduped = []
  for i in l:
    if i not in deduped:
      deduped.append(i)
  return deduped

def get_str_field(record, args):
  '''
  Return the Marc field defined by `args` within `record`
  @args:
    {obj} record: an object that defines the Marc field to parse
      number: the Marc field number to parse (if any)
      numbers: the Marc field numbers to parse (if any)
      letter: the Marc field letter to parse (if any)
      field_type: the type of object to be stored for this Marc
        field (e.g. str, list)
  @returns:
    {str} a string with the content of the requested Marc field
  '''
  number = args['number']
  letter = args['letter']
  return record.get(number, {}).get(letter, [''])[0]
