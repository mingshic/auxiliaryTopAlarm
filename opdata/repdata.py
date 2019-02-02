#!/usr/bin/env python

import time
from .top_config.req_resptop import reqtop_ready
from .config import To_top_field
from .mainformat.entrance import enter_ready 
import re
import pandas as pd

req = reqtop_ready()
pattern = enter_ready()
devicevalue = None

class reqtopdata:
    def __init__(self):
        self.s1 = pd.Series()
        self.s1.index = []

    def wdataframe(self, email, config_data):
        self.s1 = pd.Series([config_data])
        self.s1.index = [email]
        return self.s1

    def adataframe(self, email, config_data):
        s2 = pd.Series([config_data])
        s2.index = [email]
        self.s1 = self.s1.append(s2)
        return self.s1

    def dataframe(self, email):
        try:
            return self.s1[email]
        except:
            return False

    def configureInit(self, pending_data):
        emails = []
        for i in range(len(pending_data)):
            emails.append(pending_data[i][5])
        emails = list(set(emails))
        [emails.remove('') for i in range(emails.count(''))]
        for i in range(len(emails)):
            config_data = req.config_data(emails[i])
            if i == 0:
                self.s1 = self.wdataframe(emails[i], config_data)
            else:
                self.s1 = self.adataframe(emails[i], config_data)

    def reqtop(self, in_data, one_pending_data):
        null = None
        email = one_pending_data[5]
        ifindataframe = self.dataframe(email)
        if ifindataframe is False:
            config_data = req.config_data(email)
            update_in_data = self.getkey(eval(config_data), in_data, one_pending_data)
#            if len(self.s1) == 0:
#                self.s1 = self.wdataframe(email, config_data)
#            else:
#                self.s1 = self.adataframe(email, config_data)
                
        else:
            config_data = ifindataframe  
            update_in_data = self.getkey(eval(config_data), in_data, one_pending_data)
        return update_in_data


    def getkey(self, data, in_data, one_pending_data):
        titcontentinfo = self.gettitlecontent(in_data, one_pending_data)
        if data["code"] == "1":
            deviceinfo, partsconfig = self.getdeviceinfo(data["keywordInfo"], in_data, one_pending_data)
            sninfo = self.getsninfo(data["snInfo"], in_data, one_pending_data)

            partsinfo = self.getpartsinfo(partsconfig, in_data, one_pending_data, sninfo["repProjectId"])
            levelinfo = self.getlevelinfo(data["levelInfo"], in_data, one_pending_data, sninfo["repProjectId"])
#            levelinfo = self.getlevelinfo(data["levelInfo"], in_data, one_pending_data, None)
            proinfo = self.getproinfo(data["proInfo"], in_data, one_pending_data, sninfo["repProjectId"])
            if deviceinfo is not None:
                in_data.update(deviceinfo)
            if sninfo is not None:
                in_data.update(sninfo)
            if levelinfo is not None:
                in_data.update(levelinfo)
            if proinfo is not None:
                in_data.update(proinfo)
            if partsinfo is not None:
                in_data.update(partsinfo)
            if titcontentinfo is not None:
                in_data.update(titcontentinfo)
            return in_data
        elif data["code"] == "0":
            if titcontentinfo is not None:
                in_data.update(titcontentinfo)
            return in_data


    def getdeviceinfo(self, data, in_data, one_pending_data):
        global devicevalue
        keyword = {}
        devicekey, devicevalue, partsconfig = pattern.explainidentification(data, one_pending_data)
        keyword.update({"repDeviceName": devicekey})
#        keyword.update({"reqBadParts": parts})
        return keyword, partsconfig

    def getsninfo(self, data, in_data, one_pending_data):
        info = {}
        if devicevalue == None:
            info.update({"repCity": None})
            info.update({"repFactoryName": None})
            info.update({"repModelName": None})
            info.update({"repProjectId": None})
            info.update({"repSn": None})
            return info
        else:
            for i in range(len(data)):
                for j in range(len(devicevalue)):
                    if data[i]["ALERT_HOST"] == devicevalue[j]:
                        info.update({"repCity": data[i]["CITY"]})
                        info.update({"repFactoryName": data[i]["FACTORY_NM"]})
                        info.update({"repModelName": data[i]["MODEL_NAME"]})
                        info.update({"repProjectId": data[i]["PROJECT_ID"]})
                        info.update({"repSn": data[i]["SN"]})
                        return info
            info.update({"repCity": None})
            info.update({"repFactoryName": None})
            info.update({"repModelName": None})
            info.update({"repProjectId": None})
            info.update({"repSn": None})

            return info

    def getpartsinfo(self, data, in_data, one_pending_data, projectid):
        partskeyword = {}
        parts = pattern.partsidentification(data, one_pending_data, projectid)
        partskeyword.update({"reqBadParts": parts})
        return partskeyword

    def getlevelinfo(self, data, in_data, one_pending_data, projectid):
        level = {}
        alertlevel = pattern.alertexplainlevel(data, one_pending_data, projectid)
        level.update({"reqAlertLevel": alertlevel}) 
        return level

    def getproinfo(self, data, in_data, one_pending_data, projectid):
        pro = {}
        cust_id = []
        repproject_id = []
        for i in range(len(data)):
            if data[i]["PROJECT_ID"] == projectid:
                pro.update({"repCustId": data[i]["CUST_ID"]})
                pro.update({"repCustName": data[i]["CUST_NAME"]})
                pro.update({"repProjectId": data[i]["PROJECT_ID"]})
                pro.update({"repProjectName": data[i]["PROJECT_NAME"]})
                #print (pro)
                return pro
            else:
                cust_id.append(data[i]["CUST_ID"])
                repproject_id.append(data[i]["PROJECT_ID"])
                pro.update({"repCustName": data[i]["CUST_NAME"]})
                pro.update({"repProjectName": data[i]["PROJECT_NAME"]})
        if len(set(cust_id)) >= 2:
            pro.update({"repCustId": 0})
            pro.update({"repCustName": "多客户"})
        else:
            pro.update({"repCustId": cust_id[0]})
        if len(repproject_id) >= 2:
            pro.update({"repProjectId": 0})
            pro.update({"repProjectName": "多项目"})
        else:
            pro.update({"repProjectId": repproject_id[0]})
        #time.sleep(0.3)
        #print (pro)
        
        return pro

    def gettitlecontent(self, in_data, one_pending_data):
        titlecontent = {}
        titlecontent.update({"reqAlertTitle": one_pending_data[3]})
        titlecontent.update({"reqAlertContent": one_pending_data[2]})   
        titlecontent.update({"reqAlertFrom": pattern.judgealertfrom(in_data, one_pending_data[2])})
        return titlecontent
