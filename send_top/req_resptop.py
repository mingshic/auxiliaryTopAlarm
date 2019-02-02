#!/usr/bin/env python

import sys
import re
import hashlib
import time
import requests
from url import view_url
import pandas as pd
from config import time_interval 
from intervalfilter import intervalclass
from selfcomparison import Dataselfcompare
from loggings import Logger

sys.path.append("..")
from opdata.top_config.req_resptop import reqtop_ready
from model.execute_command import command_ready

ifemail_req = reqtop_ready()
interval = intervalclass() 
reqlog = Logger().getlog()

class reqtop_ready:
    def __init__(self):
        self.s1 = pd.Series()
        self.s1.index = []

    def wdataframe(self, email, config_data):
        self.s1 = pd.Series([config_data])
        self.s1.index = [email]
#        print (self.s1)
        return self.s1

    def adataframe(self, email, config_data):
        s2 = pd.Series([config_data])
        s2.index = [email]
        self.s1 = self.s1.append(s2)
#        print ("wwwwwwwwwwww", s2)
#        print ("qqqqqqqqqqqqqq", self.s1)
        return self.s1

    def dataframe(self, email):
        try:
#            print (self.s1[email])
            return self.s1[email]
        except:
            return False
    
    def filterforneed(self, data):
        null = None
        need = []
        time_interval_list = []
        for i in range(len(data)): 
            email = data[i]["email"]
            ifindataframe = self.dataframe(email)
           # print (ifindataframe)
            if ifindataframe is False:
                rep = eval(ifemail_req.config_data(email))
                if rep["code"] == "1":
#                    print (rep)
                    time_interval_list.append(rep["mergeInfo"][0]["MERGE_PERIOD"])
                    need.append(data[i])
                    if len(self.s1) == 0:
                        self.s1 = self.wdataframe(email, rep)
                    else:
                        self.s1 = self.adataframe(email, rep)
                else:
                    connectdb = command_ready()
                    connectdb.update_analysis_data(data[i]["reqanalysisId"],"2")
                    reqlog.info([data[i], "2", "mail no configure and don't send top"])
                    pass
            else:
                rep = ifindataframe
                time_interval_list.append(rep["mergeInfo"][0]["MERGE_PERIOD"])
                need.append(data[i])    
#        print (need)
        duplicate_removal_data, after_selfcompare_need, t_interval_list = Dataselfcompare(need, time_interval_list)
        interval_need = interval.inter_filter(t_interval_list, after_selfcompare_need, duplicate_removal_data)
        
#        return need
        return interval_need
       

    def norm_data(self, data):
        norm = re.compile(".*Id")
        for key,value in data.items():
            if value == 'None':
                data[key] = 'null'
            if norm.findall(key):
                if str(value).isdigit():
                    data[key] = int(value)
                else:
                    data[key] = int(0)
            if key == 'city':
                if str(value).isdigit():
                    data[key] = int(value)
                else:
                    data[key] = int(0)
        return data

    def tidy_data(self, data):
        _data = {}
        _data.update({"alertTime": data["alertTime"]})
        _data.update({"alertLevel": data["reqAlertLevel"]})
        _data.update({"alertTitle": data["reqAlertTitle"]})
        _data.update({"alertContent": data["reqAlertContent"]})
        _data.update({"alertFrom": data["reqAlertFrom"]})
        _data.update({"dealStatus": 5 if data["Sn"] == "未匹配" or data["Sn"] == "NULL" else 1})
        _data.update({"deviceName": data["repDeviceName"]})
        _data.update({"badParts": data["reqBadParts"]})
        _data.update({"city": data["repCity"]})
        _data.update({"sn": data["Sn"]})
        _data.update({"analysisId": data["reqanalysisId"]})
        _data.update({"custId": data["repCustId"]})
        _data.update({"custName": data["CustomerName"]})
        _data.update({"projectName": data["repProjectName"]})
        _data.update({"projectId": data["repProjectId"]})
        _data.update({"factoryName": data["FactoryName"]})
        _data.update({"modelName": data["ModelName"]})

        _data = self.norm_data(_data)
        return _data
        

    def view_data(self, data):
        data_dict = {}
        clientSubmitTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        key_ = "clientSubmitTime="+data["alertTime"]+"itsMonitorMd5key"
        secret = hashlib.md5()
        secret.update(key_.encode(encoding="utf-8"))
        data_dict.update({"clientSubmitTime": data["alertTime"]})
        data_dict.update({"key": secret.hexdigest()}) 
        data_dict.update({"data": self.tidy_data(data)})
#        print (data_dict)
        r = requests.post(view_url, json=data_dict)
