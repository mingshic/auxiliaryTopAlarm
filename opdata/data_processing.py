#!/usr/bin/env python
#-*- coding: utf-8 -*-

from .opinmaildata import mailData
from .opinapidata import apiData
import hashlib
import time

opmaildata = mailData()
opapidata = apiData() 

def _type_dict(data):
    content = []
    data_content = ""
    content_id = data.pop('id')
    content.append(content_id)
    content.append(data)
    return content


def data_type(data):
    if type(data) is dict:
        data_ = _type_dict(data)
    return data_


def analysis_format_data(needed_pending_data):
    uuids = []
    datas = []
    receive_info_ids = []
    emails = []
    if needed_pending_data is not None:
        for num in range(len(needed_pending_data)):
            if needed_pending_data[num][1] == 'api':
                has_been_analysis_data, unparsed = opapidata.remove_unused_fields_api(needed_pending_data[num][2])
            elif needed_pending_data[num][1] == 'mail':
                has_been_analysis_data, unparsed = opmaildata.remove_unused_fields_mail(needed_pending_data[num][2])
            uuids.append(needed_pending_data[num][0])
            datas.append((has_been_analysis_data, unparsed))
            receive_info_ids.append(needed_pending_data[num][4])
            emails.append(needed_pending_data[num][5])
    return uuids, datas, receive_info_ids, emails


def opmail(pre_data, pending_data):
    keys, filter_in, filter_not = opmaildata.datas_key_mailField(pre_data,pending_data) 
    return keys, filter_in, filter_not

