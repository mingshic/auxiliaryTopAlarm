#!/usr/bin/env /usr/local/python35/bin/python3

# -*- coding: utf8 -*-
import time
import sys
from mailprocessor import MailProcessor, deleleMail

sys.path.append('..')

from model.execute_command import command_ready
from opdata.opinmaildata import mailData

opmaildata = mailData()


def create_table():
    connectdb = command_ready()
    connectdb.create_raw_table()

def select_raw_mail_compare_id(universalID):
    connectdb = command_ready()
    ifexistid = connectdb.select_raw_mail_compare(universalID)
    return ifexistid

class Mail_raw:

    def start(self, period=30):
        while True:
            universalIDs = ""
            mail_data = MailProcessor()      
            if mail_data != []:
                for mail in mail_data[::-1]:  
               # for mail in mail_data:  
                    #print ("111111111111",mail)
                    ifid = select_raw_mail_compare_id(mail["universalID"])
                    if ifid:
                        universalIDs += mail["universalID"] + ","
                        pass
                    else:
                        try:
                            self.connectdb = command_ready()
                            self.connectdb.insert_raw_mail_data(mail, 'mail', 1) 
                            universalIDs += mail["universalID"] + ","
                        except:
                            pass
               # print (universalIDs)
                deleleMail(universalIDs)
            else:
                pass

            time.sleep(period)

def main():
    
    if True:  
        mail_raw = Mail_raw()
    else: 
        exit(1)

    mail_raw.start(20)

if __name__ == '__main__':
    create_table() 
    main()


