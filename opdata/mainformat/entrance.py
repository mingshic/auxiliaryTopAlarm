#!/usr/bin/env python

import re
import time
from .identify import idenindeal 

class enter_ready:

    def deviceinfo(self, *args):
        devicekey, devicevalue = idenindeal(args[0], args[1], args[2])
#        print (devicekey, devicevalue)
        return devicekey, devicevalue
#        return args[0], "10.1.1.0"

    def keyword(self, *args):
        try:
            for key in args[0].split(" "):
                if key in args[1] or key in args[2]:
                    return True
                else:
                    return False
        except:
            pass 
        return False

    def keynum(self, *args):
        return False

    def keychar(self, *args):
        try:
            target = re.compile(args[0])
            if target.findall(args[1]) or target.findall(args[2]):
                return True
            else:
                return False
        except:
            pass
        return False

    def explainidentification(self, config, detail):
        devicekey = None
        devicevalue = None
        devicevalues = []
        partsconfig = []
        for i in range(len(config)):
            if config[i]["KEY_NAME"] == "设备标识":
                devicekey, devicevalue = self.deviceinfo(config[i], detail[2], detail[3])
                if devicevalue:
                    for i in range(len(devicevalue)):
                        devicevalues.append(devicevalue[i])
                else:
                    pass
            else:
                partsconfig.append(config[i])
        values = list(set(devicevalues))
        return devicekey, values, partsconfig


    def partsidentification(self, config, detail, projectid):
        parts = []
        for i in range(len(config)):
            if config[i]["PROJECT_ID"] == projectid:
                if self.keyword(config[i]["KEY_WORD"], detail[2], detail[3]):
                    parts.append(config[i]["KEY_NAME"])
                if self.keynum(config[i]["KEY_NUM"], detail[2], detail[3]):
                    parts.append(config[i]["KEY_NAME"])
                if self.keychar(config[i]["KEY_CHAR"], detail[2], detail[3]):
                    parts.append(config[i]["KEY_NAME"])
        parts = list(set(parts))
        if " ".join(parts) == "":
            parts = None
            return parts
        else:
            return " ".join(parts)
        
    def alertlevel(self, *args):
        try:
            for key in args[0].split(" "):
                if key in args[1] or key in args[2]:
                    return True
                else: 
                    pass
        except:
            pass
        return False
    
    def syntheticlevel(self, args):
        if "紧急" in args:
            return "紧急"
        elif "主要" in args:
            return "主要"
        elif "次要" in args:
            return "次要"
        elif "警告" in args:
            return "警告"
        elif "维护" in args:
            return "维护"
        elif "正常" in args:
            return "正常"
   
    def alertexplainlevel(self, config, detail, projectid):
        level = []
        alarm_urgent = []
        alarm_main = []
        alarm_secondary = []
        alarm_warning = []
        alarm_maintain = []
        alarm_normal = []
        filter_projectid_level = []
        for i in range(len(config)):
            if config[i]["PROJECT_ID"] == projectid:
                filter_projectid_level.append(config[i])
            elif config[i]["ALERT_LEVEL"] == "紧急":
                alarm_urgent.append(config[i])
            elif config[i]["ALERT_LEVEL"] == "主要":
                alarm_main.append(config[i])
            elif config[i]["ALERT_LEVEL"] == "次要":
                alarm_secondary.append(config[i])
            elif config[i]["ALERT_LEVEL"] == "警告":
                alarm_warning.append(config[i])
            elif config[i]["ALERT_LEVEL"] == "维护":
                alarm_maintain.append(config[i])
            elif config[i]["ALERT_LEVEL"] == "正常":
                alarm_normal.append(config[i])

        if filter_projectid_level:
            for i in range(len(filter_projectid_level)):
                if self.alertlevel(filter_projectid_level[i]["ALERT_KEYWORD"], detail[2], detail[3]):
                    level.append(filter_projectid_level[i]["ALERT_LEVEL"])
            syntheticlevel = self.syntheticlevel(level)
            return syntheticlevel
        else:
            for i in range(len(alarm_urgent)):
                if self.alertlevel(alarm_urgent[i]["ALERT_KEYWORD"], detail[2], detail[3]):
                    level.append(alarm_urgent[i]["ALERT_LEVEL"])
                    break
            for i in range(len(alarm_main)):
                if self.alertlevel(alarm_main[i]["ALERT_KEYWORD"], detail[2], detail[3]):
                    level.append(alarm_main[i]["ALERT_LEVEL"])
                    break
            for i in range(len(alarm_secondary)):
                if self.alertlevel(alarm_secondary[i]["ALERT_KEYWORD"], detail[2], detail[3]):
                    level.append(alarm_secondary[i]["ALERT_LEVEL"])
                    break
            for i in range(len(alarm_warning)):
                if self.alertlevel(alarm_warning[i]["ALERT_KEYWORD"], detail[2], detail[3]):
                    level.append(alarm_warning[i]["ALERT_LEVEL"])
                    break
            for i in range(len(alarm_maintain)):
                if self.alertlevel(alarm_maintain[i]["ALERT_KEYWORD"], detail[2], detail[3]):
                    level.append(alarm_maintain[i]["ALERT_LEVEL"])
                    break
            for i in range(len(alarm_normal)):
                if self.alertlevel(alarm_normal[i]["ALERT_KEYWORD"], detail[2], detail[3]):
                    level.append(alarm_normal[i]["ALERT_LEVEL"])
                    break
            syntheticlevel = self.syntheticlevel(level)
            return syntheticlevel

#    def match_indata(self, data):

    def judgealertfrom(self, in_data, alertcontent):
        num = 0
        for key,value in in_data.items():
            if str(value) in str(alertcontent):
                num += 1
            else:
                pass
        if num >= 4:
            return "smart"
        elif in_data["mailCustomerName"] is not None:
            return in_data["mailCustomerName"]
        else:
            return in_data["email"]
              

#    def explainsn(self, config, devicevalue, detail):
#        if devicevalue == 
#        for i in range(len(config)):
#            if config[i]["ALERT_HOST"] == devicevalue:
                 

