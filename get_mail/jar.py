# -*- coding: utf8 -*-


import jpype 
import os

class Jarmail:
    def __init__(self):        
        self.jarpath = os.path.join(os.path.abspath('.'), 'jar/dc.jar')
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % self.jarpath)
        self.dcNotes = jpype.JClass('com.wbm.dcnotes.DcNotesManager')

    def get_data(self, args):
        self.req = self.dcNotes()
        data = self.req.receive(str(args))
        jpype.shutdownJVM()
        return data


#if __name__ == "__main__":
#    a = Jarmail()
#    data = a.get_data({'appsecret': '71D4550CD969F58ED9F2975A675E5A31', 'universalID': '4A18AF243D5857F86834C3C0E149DBA9','appid': 'dcitsMonitor', 'accesstime': '2018-11-05 06:28:50'})
