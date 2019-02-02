#!/usr/bin/env python

import sys
import time
import re
from config import remove_content_field
from loggings import Logger

sys.path.append("..")
from model.execute_command import command_ready
interlog = Logger().getlog()

class intervalclass:

    def rematch(self, match):
        return re.compile(match)

    def remove(self, data, email):
        if email in remove_content_field:
            match = self.rematch(remove_content_field[email])
            matched = match.findall(data)
            try:
                if matched:
                    return "".join(data.split(matched[0]))
            except:
                pass
        
        elif "smart" in remove_content_field:
            match = self.rematch(remove_content_field["smart"])
            matched = match.findall(data)
            try:
                if matched:
                    return "".join(data.split(matched[0]))
            except:
                pass 
            
                        
        return None
    def ifabandon(self, data, interval_data):
        now_data = self.remove(data["reqAlertContent"], data["email"])
        if now_data is not None:
            for i in range(len(interval_data)):
    #            if 判断email是否在remove_content_field
                origin_interval_data = self.remove(interval_data[i]["reqAlertContent"], interval_data[i]["email"])
                if now_data == origin_interval_data and data["reqAlertTitle"] == interval_data[i]["reqAlertTitle"]:
                    connectdb = command_ready()
                    connectdb.update_interval_filtered_analysis(data, "3")
                    interlog.info([data, "3", "inter time"])
                    return None
                else:
                    pass
            return data
        elif now_data is None:
            for i in range(len(interval_data)):
                if data["reqAlertContent"] == interval_data[i]["reqAlertContent"] and data["reqAlertTitle"] == interval_data[i]["reqAlertTitle"]:
                    connectdb = command_ready()
                    connectdb.update_interval_filtered_analysis(data, "3")
                    interlog.info([data, "3", "inter time"])
                    return None
#                elif data["reqAlertContent"] != interval_data[i]["reqAlertContent"] and data["reqAlertTitle"] == interval_data[i]["reqAlertTitle"]:
                else:
                    pass
            return data
        
                
    def reset_data_deal(self, data):
        for i in range(len(data)):
            connectdb = command_ready()
            connectdb.update_interval_filtered_analysis(data[i], "4")
            interlog.info([data[i], "4", "duplicate set"])

  
    def inter_filter(self, interval, data, reset_data):
        interval_time = interval
        inter_data = []
        self.reset_data_deal(reset_data)
        for i in range(len(data)):
            interval_data = []
            connectdb = command_ready()
            retain = connectdb.select_interval_time_analysis(int(interval_time[i]), data[i]["email"], "2")

            abandonifdata = self.ifabandon(data[i], retain)
            if abandonifdata is None:
                pass
            else: 
                inter_data.append(abandonifdata)
        return inter_data
