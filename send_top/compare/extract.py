#!/usr/bin/env python

import time
import datetime

def mailRepChoise(_data):
    if _data["FactoryName"] == 'None':
        _data["FactoryName"] = "未匹配"
    if _data["ModelName"] == 'None':
        _data["ModelName"] = "未匹配"
    if _data["Sn"] == 'None':
        _data["Sn"] = "未匹配"
    if _data["reqBadParts"] == 'None':
        _data["reqBadParts"] = "未匹配"
    if _data["CustomerName"] == 'None':
        _data["CustomerName"] = "未匹配"
    if _data["reqAlertLevel"] == 'None':
        _data["reqAlertLevel"] = "未匹配"
    if _data["repDeviceName"] == 'None':
        _data["repDeviceName"] = "未匹配"
    return _data

def choisefield(data):
    send_data = []
    for i in range(len(data)):
        _data = {}
        _data.update({"reqanalysisId": data[i]['reqanalysisId']})
        _data.update({"CustomerName": data[i]['repCustName'] if data[i]['repCustName'] != 'None' else data[i]['mailCustomerName']})
        _data.update({"reqAlertContent": data[i]['reqAlertContent']})
        _data.update({"reqAlertLevel": data[i]['reqAlertLevel']})
        _data.update({"reqAlertTitle": data[i]['reqAlertTitle']})
        _data.update({"reqAlertFrom": data[i]['reqAlertFrom']})
        _data.update({"alertTime": data[i]['alertTime']})
        _data.update({"repDeviceName": data[i]['repDeviceName']})
        _data.update({"reqBadParts": data[i]['reqBadParts']})
        _data.update({"repCity": data[i]['repCity']})
        _data.update({"repCustId": data[i]['repCustId']})
        _data.update({"repProjectName": data[i]['repProjectName']})
        _data.update({"repProjectId": data[i]['repProjectId']})
        _data.update({"FactoryName": data[i]['repFactoryName'] if data[i]['repFactoryName'] != 'None' else data[i]['mailFactoryName']})
        _data.update({"ModelName": data[i]['repModelName'] if data[i]['repModelName'] != 'None' else data[i]['mailModelName']})
        _data.update({"Sn": data[i]['repSn'] if data[i]['repSn'] != 'None' else data[i]['mailSn']})
        _data.update({"dealStatus": data[i]['dealStatus']})
        _data.update({"email": data[i]['email']})
        _data.update({"analysisedTime": data[i]['analysisedTime']})
        send_data.append(mailRepChoise(_data))
    return send_data 
