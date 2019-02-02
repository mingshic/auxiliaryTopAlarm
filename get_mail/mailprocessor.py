#!/usr/bin/python
import time

import sys
from settings import json_initialization, appid, appkey
from url import url, del_url
import requests
#from jar import Jarmail

sys.path.append("..")

from model.execute_command import command_ready


def MailProcessor():
    req_data = json_initialization(appid, appkey)
    json = req_data.json

#    json['universalIDs'] = 100
    json["fetchSize"] = 100
    req = eval(requests.post(url, json=json).text)
    if int(req['code']) == 200:
        mail_data = req['data']
        return mail_data
    elif int(req['code']) == 10:
        mail_data = []
        return mail_data 

def deleleMail(universalIDs):
    req_data = json_initialization(appid, appkey)
    json = req_data.json
    json["universalIDs"] = universalIDs
    req = eval(requests.post(del_url, json=json).text)
    

#    connectdb = command_ready()
#    try:
#
#        last_uids = connectdb.select_raw_mail_uid('mail')
#    except:
#        last_uids = []

#    if len(last_uids) != 0:
#        mail_data_filter = []
#        universalID = last_uids[0][-1]
##        json['universalID'] = universalID
#        json['id'] = "4089DE59C106D28B0435BBF605A3FBD5"
#    
#        req = eval(requests.post(url, json=json).text)
#        print ("last",req)
#        if int(req['code']) == 200:
#            mail_data = req['data'] 
#            return mail_data
    
#    else:
#        req = eval(requests.post(url, json=json).text)
#        print ("test",req)
#        if int(req['code']) == 200:
#            mail_data = req['data']
#            return mail_data       

