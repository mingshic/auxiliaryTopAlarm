#!/usr/bin/env python

import time
from intervalfilter import intervalclass


selfcompare = intervalclass()


def Dataselfcompare(data, time_interval_list):
    selfdatalist = []
    selfdata = {}
    num = 0
    for i in range(len(data)):
        selfcompdata_data = selfcompare.remove(data[i]["reqAlertContent"], data[i]["reqAlertFrom"])
        selfdata.update({str(data[i]["reqAlertTitle"])+"-"+str(selfcompdata_data): data[i]})
        num += 1
        if num > len(selfdata):
            time_interval_list.pop(num-1)
            num = len(selfdata)
            
    for key,value in selfdata.items():
        data.remove(value)
        selfdatalist.append(value)

    return data, selfdatalist, time_interval_list
