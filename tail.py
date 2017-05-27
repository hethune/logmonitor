#!/usr/bin/env python

'''
Python-Tail - Unix tail follow implementation in Python. 

python-tail can be used to monitor changes to a file.

Example:
  import tail

  # Create a tail instance
  t = tail.Tail('file-to-be-followed')

  # Register a callback function to be called when a new line is found in the followed file. 
  # If no callback function is registerd, new lines would be printed to standard out.
  t.register_callback(callback_function)

  # Follow the file with 5 seconds as sleep time between iterations. 
  # If sleep time is not provided 1 second is used as the default time.
  t.follow(s=5) 
'''

import os
import re
import sys
import time

RULE = '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
INTERVAL = 10

class Tail(object):
  ''' Represents a tail command. '''
  def __init__(self, tailed_file):
    ''' 
    Initiate a Tail instance.
    Check for file validity, assigns callback function to standard out.
        
    Arguments:
      tailed_file - File to be followed. 
    '''
    self.check_file_validity(tailed_file)
    self.tailed_file = tailed_file
    self.callback = sys.stdout.write

  def follow(self, s=1):
    ''' 
    Do a tail follow. If a callback function is registered it is called with every new line. 
    Else printed to standard out.

    Arguments:
      s - Number of seconds to wait between each iteration; Defaults to 1. 
    return contains failed and Complete exception block.
    '''

    flag = False
    exceptionContent = ''
    exceptionCount = 0
    last_time = time.time()
    with open(self.tailed_file) as file_:
      # Go to the end of file
      file_.seek(0,2)
      while True:
        curr_position = file_.tell()
        line = file_.readline()
        if not line:
          file_.seek(curr_position)
          time.sleep(s)
          if time.time() - last_time > INTERVAL and 'Exception' in exceptionContent:
            exceptionContent, flag = self.back(exceptionContent)
        else:

          last_time = time.time()
          #get contains exception line
          if 'Exception' in line:
            exceptionCount += 1
            if exceptionCount > 1:
              exceptionContent = self.back(exceptionContent)[0]
            exceptionContent += line 
            flag = True
            continue
          # get Complete exception block
          if flag == True:
            if re.search(RULE, line):
              exceptionContent, flag = self.back(exceptionContent)
              continue
            exceptionContent += line
          # other line
          if flag == False:
            self.callback(line)

  def back(self, content):
    self.callback(content)
    exceptionContent = ''
    flag = False
    return (exceptionContent, flag)

  def register_callback(self, func):
    ''' Overrides default callback function to provided function. '''
    self.callback = func

  def check_file_validity(self, file_):
    ''' Check whether the a given file exists, readable and is a file '''
    if not os.access(file_, os.F_OK):
      raise TailError("File {} does not exist".format(file_))
    if not os.access(file_, os.R_OK):
      raise TailError("File {} not readable".format(file_))
    if os.path.isdir(file_):
      raise TailError("File {} is a directory".format(file_))

class TailError(Exception):
  def __init__(self, msg):
    self.message = msg
  def __str__(self):
    return self.message
