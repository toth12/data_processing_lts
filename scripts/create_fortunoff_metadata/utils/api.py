#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
API for db connections
'''

from pymongo import MongoClient

##
# Globals
##

config = {
  'protocol': 'http',
  'host': 'localhost',
  'port': 8080,
  'db': 'lts'
}

##
# Functions
##

def get_client(host='localhost', port=27017):
  '''
  Get a MongoDB client
  @returns:
    {MongoClient} a MongoClient object
  '''
  return MongoClient(host, port, connect=False)

def save(obj, table):
  '''
  Save `obj` in the `table` table of `db`
  @args:
    {obj|list} the object or objects to save
    {str} the table name where save should be directed
  '''
  if isinstance(obj, list):
    result = db[table].insert_many(obj)
  else:
    result = db[table].insert_one(obj)
  return result

db = get_client()[config['db']]
