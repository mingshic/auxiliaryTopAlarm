#!/usr/local/python35/bin/python3
#-*- coding: utf-8 -*-


import sys
import time
from req_resptop import reqtop_ready
from compare.extract import choisefield
from loggings import Logger

sys.path.append('..')

from model.execute_command import command_ready
from model.settings import Tables

import requests

req_top = reqtop_ready()
sendlog = Logger().getlog()

def update_analysis_data_status(info_id, deal_status):
    connectdb = command_ready()
    connectdb.update_analysis_data(info_id, deal_status)

def update_analysis_data_all(deal_status):
    connectdb = command_ready()
    connectdb.update_analysis_data_status_all(deal_status)

class send_data:
    def _process(self):
        self.connectdb = command_ready()
        req_pending_data = self.connectdb.select_analysis_data("1")
         
        send_data = choisefield(req_pending_data)
        send_data_need = req_top.filterforneed(send_data)
        return send_data_need

    def start(self, period=30):
        while True:
###########告警至top
            send_data = self._process()   
#            print (send_data)
            for i in range(len(send_data)):
                req_top.view_data(send_data[i])
                update_analysis_data_status(send_data[i]["reqanalysisId"],"2")
                sendlog.info([send_data[i], "2", "send top"])
            time.sleep(period)
            
            

def main():
    if True:
        send_to = send_data()
    else:
        exit(1)
    
    send_to.start(20)


if __name__ == '__main__':
    main()
 
