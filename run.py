#!/usr/bin/env python

''' 
Does a tail follow against monitorlog/err.log with a time interval of 5 seconds.
Prints recieved new lines to standard out 
'''

import re
import json
import tail
import yaml
import requests

with open('config.yml') as f:
  config = yaml.load(f)

def return_line(msg):
  ''' Prints received text '''
  for pattern_item in config['sending_patterns']:
    if [x for x in pattern_item['stop_words'] if x in msg]:
      if len(msg) > config['msglength']:
        msg = msg[0:config['msglength']]
      send_msg(msg, pattern_item['recipients'])
   
def send_msg(msg, recipients):
  values = {'recipients' : recipients,
          'msg' : msg
  }
  url = config['request_url']
  headers = {'Content-Type': 'application/json'}
  data = json.dumps(values)
  req = requests.post(url, data, headers=headers)

t = tail.Tail(config['logpath'])
t.register_callback(return_line)
t.follow(s=1)

