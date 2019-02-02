#!/usr/local/python35/bin/python3
#-*- coding: utf-8 -*-

import sys
import time
import logging

sys.path.append('..')

from model.execute_command import command_ready
from model.settings import Tables
from opdata.data_processing import analysis_format_data, opmail 
#from app.model.execute_command import insert_analysis_data

logging.basicConfig(level=logging.DEBUG,
                    format='levelname:%(levelname)s filename: %(filename)s '
                           'outputNumber: [%(lineno)d]  thread: %(threadName)s output msg:  %(message)s'
                           ' - %(asctime)s', datefmt='[%d/%b/%Y %H:%M:%S]',
                    filename='./format_raw_data.log')

def analysis_if_success_todb(receive_info_id, analysis_flg):
    connectdb = command_ready()
    connectdb.update_raw_alarm(receive_info_id, analysis_flg)
    

def create_format_table():
    connectdb = command_ready()
    connectdb.create_analysis_table()

class Analysis_data:
    def _process(self):
        self.connectdb = command_ready()
        pending_data = self.connectdb.select_raw_alarm(Tables['receive_table'], 0)
        
        uuids, processed_data, receive_info_ids, emails = analysis_format_data(pending_data)

        keys, filter_data_in_field, filter_data_not_in_field = opmail(processed_data,pending_data)
        return keys, filter_data_in_field, receive_info_ids

    def start(self, period=30):
        while True:
            source_type, datas, receive_info_ids = self._process()

            for i in range(len(datas)):            
                self.connectdb = command_ready()
                self.connectdb.insert_analysis_data(datas[i],receive_info_ids[i])   
                logging.info(datas[i])
                analysis_if_success_todb(receive_info_ids[i], 1)      
            
            time.sleep(period)

            
            

def main():
    if True:
        analysis = Analysis_data()
    else:
        exit(1)
    
    analysis.start(15)


if __name__ == '__main__':
    create_format_table()
    main()
 
