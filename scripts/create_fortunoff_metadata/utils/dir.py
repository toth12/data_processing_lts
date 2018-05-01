#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Directory helpers
'''

import os
from shutil import rmtree

def make_dir(_dir):
  '''
  Try to make a directory on disk
  '''
  try:
    os.makedirs(_dir)
  except Exception:
    pass

def rm_dir(_dir):
  '''
  Try to remove a directory on disk
  '''
  try:
    rmtree(_dir)
  except Exception:
    pass
