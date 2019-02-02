#-*- coding: utf-8 -*-
#!/usr/bin/env python
import sys
import hashlib
import time
import datetime

from .settings import Tables
from .model import MysqlDB
from .sql import create_raw_table_sql, create_analysis_table_sql#, create_customer_system_table_sql, create_rule_table_sql,  create_case_matched_table_sql

import pickle


class command_ready(MysqlDB):
    def __init__(self):
        super(command_ready,self).__init__()
        self.conn = self.connection

    def operation_close(self):
        self.conn.connection.commit()
        self.conn.connection.close()

    def create_raw_table(self):
        self.conn.execute(create_raw_table_sql)


    def create_rule_table(self):
        self.conn.execute(create_rule_table_sql)
        self.conn.execute(create_case_matched_table_sql)

    def create_analysis_table(self):
        self.conn.execute(create_analysis_table_sql)

    def create_customer_system_table(self): 
        self.conn.execute(create_customer_system_table_sql)


    def select_raw_mail_uid(self, source_type):
        sql = '''select uuid from %s where sourceType='%s' order by receiveInfoId desc limit 1 ''' % (Tables['receive_table'],source_type)
        conn = self.conn
        conn.execute(sql)
        uuid = conn.fetchall()
        conn.connection.commit()
        conn.connection.close()
        return uuid


    def update_raw_alarm(self, receive_info_id, analysis_flg):
        sql = '''update %s set analysisFlg='%s' where receiveInfoId='%s' ''' % (Tables["receive_table"],analysis_flg,receive_info_id)
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()

    def insert_analysis_data(self, data, receive_info_id):
        deal_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = '''insert into %s (receiveInfoId,mailCustomerName,email,repCustName,mailMonitorName,mailMonitorVersion,identityCode,kpiAssortment,kpiName,kpiValue,mailAlertContent,reqAlertContent,reqAlertLevel,reqAlertTitle,reqAlertFrom,alertTime,mailIp,repDeviceName,reqBadParts,repCustId,repProjectName,repProjectId,serviceObject,serviceName,repFactoryName,mailFactoryName,mailModelName,repModelName,repSn,mailSn,repCity,mailCity,businessSystem,maDept,maUser,maMobile,maEmail,analysisedTime,dealStatus) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (Tables["format_table"],receive_info_id,data["mailCustomerName"],data['email'],data["repCustName"],data["mailMonitorName"],data["mailMonitorVersion"],data["identityCode"],data["kpiAssortment"],data["kpiName"],data["kpiValue"],data["mailAlertContent"],data["reqAlertContent"],data["reqAlertLevel"],data["reqAlertTitle"],data["reqAlertFrom"],data["alertTime"],data["mailIp"],data["repDeviceName"],data["reqBadParts"],data["repCustId"],data["repProjectName"],data["repProjectId"],data["serviceObject"],data["serviceName"],data["repFactoryName"],data["mailFactoryName"],data["mailModelName"],data["repModelName"],data["repSn"],data["mailSn"],data["repCity"],data["mailCity"],data["businessSystem"],data["maDept"],data["maUser"],data["maMobile"],data["maEmail"],deal_time,"1")
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()

    def select_raw_alarm(self, pending_table, analysis_flg):
        sql = '''select uuid,sourceType,receiveContent,receiveTitle,receiveInfoId,email,arrivalTime from %s where analysisFlg='%s' ''' % (pending_table,analysis_flg)
        conn = self.conn
        nums = conn.execute(sql)
        penging_data = conn.fetchall()
        conn.connection.commit()
        conn.connection.close()
        return penging_data
        

    def select_analysis_data(self, deal_status):
        #sql = '''select reqanalysisId,repCustName,reqAlertContent,reqAlertLevel,reqAlertTitle,reqAlertFrom,alertTime,repDeviceName,reqBadParts,repCity,repCustId,repProjectName,repProjectId,repFactoryName,repModelName,repSn,dealStatus from %s where dealStatus='%s' ''' % (Tables["format_table"], deal_status)
        sql = '''select * from %s where dealStatus='%s' limit 100 ''' % (Tables["format_table"], deal_status)
        conn = self.conndict
        conn.execute(sql)
        penging_data = conn.fetchall()
        conn.connection.commit()
        conn.connection.close()
        return penging_data
    
    def select_analysis_data_interval_filter(self, email):
        sql = '''select * from %s where email='%s' ''' % (Tables["format_table"], email)
        conn = self.conn
        conn.execute(sql)
        penging_data = conn.fetchall()
        conn.connection.commit()
        conn.connection.close()
        return penging_data

    def select_interval_time_analysis(self, interval_time, email, deal_status):
        sql = '''select * from %s where email='%s' and alertTime >= DATE_SUB(NOW(), INTERVAL %d MINUTE) and dealStatus='%s' ''' % (Tables["format_table"], email, interval_time, deal_status)
        conn = self.conndict
        conn.execute(sql)
        penging_data = conn.fetchall()
        conn.connection.commit()
        conn.connection.close()
        return penging_data

    def update_interval_filtered_analysis(self, data, deal_status):
        sql = '''update %s set dealStatus='%s' where reqanalysisId='%s' ''' % (Tables["format_table"],deal_status,data["reqanalysisId"])
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()
   
    def update_analysis_data(self, info_id, deal_status):
        sql = '''update %s set dealStatus='%s' where reqanalysisId='%s' ''' % (Tables["format_table"],deal_status,info_id) 
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()

    def update_analysis_data_status_all(self, deal_status):
        sql = '''update %s set dealStatus='%s' ''' % (Tables["format_table"],deal_status)
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()


    def choisemail(self, sendto, fromcome):
        if sendto == "<service_request@dcits.com>" or sendto == "service_request@dcits.com" or sendto == "":
            if len(fromcome.split(" ")) == 2:
                return fromcome.split(" ")[1].replace('"',"").replace(">","").replace("<","")
            else:
                return fromcome.replace('"',"").replace(">","").replace("<","")
        elif fromcome == "<service_request@dcits.com>" or fromcome == "service_request@dcits.com" or fromcome == "":
            if len(sendto.split(" ")) == 2:
                return sendto.split(" ")[1].replace('"',"").replace(">","").replace("<","")
            else:
                return sendto.replace('"',"").replace(">","").replace("<","")
        elif sendto != "<service_request@dcits.com>" or sendto != "service_request@dcits.com" or sendto != "":
            if len(sendto.split(" ")) == 2:
                return sendto.split(" ")[1].replace('"',"").replace(">","").replace("<","")
            else:
                return sendto.replace('"',"").replace(">","").replace("<","")

    def select_raw_mail_compare(self, universalID):
        sql = '''select * from %s where uuid='%s' ''' % (Tables["receive_table"],universalID)
        conn = self.conn
        conn.execute(sql)
        penging_data = conn.fetchall()
        conn.connection.commit()
        conn.connection.close()
        return penging_data


    def insert_raw_mail_data(self, mail_data, source_type, receive_type):
        sql = '''insert into %s (uuid,sourceType,email,arrivalTime,receiveType,receiveTitle,receiveContent,analysisFlg) values ('%s','%s','%s','%s','%s','%s','%s','%s')''' % (Tables["receive_table"],mail_data['universalID'],source_type,self.choisemail(mail_data['sendto'],mail_data['from']),mail_data['created'],receive_type,mail_data['subject'],mail_data['body'],"0")
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()

