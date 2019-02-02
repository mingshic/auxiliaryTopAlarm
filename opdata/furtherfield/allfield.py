#!/usr/bin/env python


import time

class needfield:
    def mailallfield(self, *args):
        if args[1] == "identityCode":
            args[0].update({args[1]: args[2]})
        elif args[1] == "email":
            args[0].update({args[1]: args[3]})
        elif args[1] == "alertTime":
#            args[0].update({args[1]: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
            args[0].update({args[1]: args[4]})
        else:
            args[0].update({args[1]: None})
        return args[0]
    
    def mailfield(self, *args):
        _key = []
        field_in = {}
        field_not_in = {}
        for key, value in args[0].items():
            if key in args[1]:
                if args[1][key] == "alertTime":
                    try:
                        if time.strptime(value, "%Y-%m-%d %H:%M:%S"):
                            field_in.update({args[1][key]: value})
                            _key.append(args[1][key]) 
                    except:
                        field_in.update({args[1][key]: args[2]}) 
                        _key.append(args[1][key])
                else:
                    field_in.update({args[1][key]: value})
                    _key.append(args[1][key])
            else:
                try:
                    field_not_in.update({args[1][key]: value})
                except:
                    pass
        return _key, field_in, field_not_in



