#!/usr/bin/env python

import time
from .repdata import reqtopdata
from .config import mailaccount
from .config import Analysis_smart_field, To_top_field
from .furtherfield.allfield import needfield

c_field = needfield()
req = reqtopdata()


class mailData:
    def remove_unused_fields_mail(self, data):
        k = []
        j = []
        unparsed = []
        data = data.split("\n")
        for i in data:
            if len(i.split(":")) == 2:
                k.append(i.split(":")[0].strip())
                if i.split(":")[1] == "":
                    j.append("None")
                else:
                    j.append(i.split(":")[1].strip())
    
            elif len(i.split(":")) > 2:
                k.append(i.split(":")[0].strip())
                if i.split(":")[1][0] == " ":
                    b = i.split(":")[1].split(" ")
                    b.remove("")
                    b = " ".join(b)
                    j.append(b+':'+':'.join(i.split(":")[2:]))
                else:
                    j.append(i.split(":")[1]+':'+':'.join(i.split(":")[2:]))
            elif len(i.split(":")) < 2:
                unparsed.append("")
    
        return dict(zip(k,j)), unparsed


    def update_toTopField(self, in_data, one_pending_data):
        updatedata = req.reqtop(in_data, one_pending_data)
        return updatedata


    def datas_key_add_toTopField(self, in_data, one_pending_data):
        for i in To_top_field:
            in_data.update({i: None})
        update_in_data = self.update_toTopField(in_data, one_pending_data)
         
        return update_in_data
    
    
    def datas_key_mailField(self, pre_data, pending_data):        
        req.configureInit(pending_data)
        keys = []
        filter_in = []
        filter_not_in = []
        for i in range(len(pre_data)):
            if len(pre_data[i]) == 2:
                _key, field_in, field_not_in = c_field.mailfield(pre_data[i][0], Analysis_smart_field, pending_data[i][6]) 
                field_in = self.datas_if_not_to_None(_key, field_in, pending_data[i][0], pending_data[i][5], pending_data[i][6])
                _field_in = self.datas_key_add_toTopField(field_in, pending_data[i])
                keys.append(_key) 
                filter_in.append(_field_in)
                filter_not_in.append(field_not_in)
        return keys, filter_in, filter_not_in
    
    
    def datas_if_not_to_None(self, keys, filter_data_in_field, uuid, email, arrivaltime):
        for key in Analysis_smart_field.keys():
            if Analysis_smart_field[key] not in keys:
                filter_data_in_field.update(c_field.mailallfield(filter_data_in_field, Analysis_smart_field[key], uuid, email, arrivaltime))
        return filter_data_in_field
    
