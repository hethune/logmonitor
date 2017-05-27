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
import logging

logger = logging.getLogger("logMonitor")
logger.setLevel(logging.INFO)
filehandler = logging.FileHandler('log_monitor.log','w')
formatter =  logging.Formatter('%(asctime)s  %(filename)s  %(levelname)s - %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',)
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)

with open('config.yml') as f:
  config = yaml.load(f)

def return_line(msg):
  ''' Prints received text '''
  logger.debug('Wechat send message [{}] \n'.format(msg.strip()))
  for pattern_item in config['sending_patterns']:
    if [x for x in pattern_item['stop_words'] if x in msg]:
      if len(msg) > config['msglength']:
        msg = msg[0:config['msglength']]
      send_msg(msg.strip(), pattern_item['recipients'])
   
def send_msg(msg, recipients):
  values = {'recipients' : recipients,
          'msg' : msg
  }
  url = config['request_url']
  headers = {'Content-Type': 'application/json'}
  data = json.dumps(values)
  req = requests.post(url, data, headers=headers)
  logger.info('Wechat send status {}, content {}'.format(req, req.text))


t = tail.Tail(config['logpath'])
t.register_callback(return_line)
t.follow(s=1)
