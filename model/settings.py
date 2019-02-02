#!/usr/bin/env python


import os


Databases = {
    "Database": "alarm",
}

class Mysqlconfig():

    ENV = 'Mysqlconfig'
    DEBUG = True

    # session
    CSRF_ENABLED = True
    SECRET_KEY = "asgSfsf3Xd8ffy]fw8vfd0zbvssqwertsd4sdwe"

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # datebase
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://alarm:123456@localhost/"+Databases['Database']+"?charset=utf8"
#    SQLALCHEMY_ECHO = True



Mysql_parameter = {
    "HOST": "localhost",
    "PORT": 3306,
    "USER": "alarm",
    "PASSWD": "123456",
    "DB": "alarm",
    "CHARSET": "utf8",
} 


Tables = {
    "rule_table": "rule_recotb",
    "receive_table": "alarm_raw_data",
    "access_use": "customer_access_use",
    "customer_system_table": "customer_system",
    "format_table": "raw_analysis_data", 
    "customer_alert_rule": "customer_alert_rule",
    "case_matched_rule": "case_matched_rule",
}
