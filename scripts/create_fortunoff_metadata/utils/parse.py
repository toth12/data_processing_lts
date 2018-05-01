#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Helpers for processing structured fields from plaintext
'''

##
# Globals
##

integers = [str(i) for i in range(10)]

##
# Functions
##

def clean_year(imprint_year):
  '''
  Read in a raw imprint year and return the first string
  of four consecutive integers from that string
  '''
  for token in imprint_year.replace(',', ', ').split(' '):
    clean_token = ''
    for character in token:
      if character in integers:
        clean_token += character
    if len(clean_token) == 4:
      return clean_token
  print('could not parse a year from', imprint_year)
  return imprint_year