#!/usr/bin/env python

import re

def idenindeal(config, content, title):
    if config["KEY_WORD"] is not None or config["KEY_NUM"] is not None or config["KEY_CHAR"] is not None:
        try:
#            if config["KEY_WORD"] in content or config["KEY_WORD"] in title:
            return indeal(config, content, title)
                #return config["KEY_WORD"], "1.1.1.1"
        except:
            pass 
        return config["KEY_WORD"], None
    return config["KEY_WORD"], None

def keynumsplit(args):
    try:
        args = args.split(" ")
        if len(args) >= 2:
            if type(args[0]) == int and type(args[1]) == int:
                return int(args[0]), int(args[1])
    except:
        pass
    return None, None 
        

def match(*args):
    return args[0].findall(args[1])

def compilematch(args):
    try:
#        args.replace('\\\\', '\\')
        target = re.compile(args)
        return target
    except:
        pass
    target = re.compile("")
    return target

def matchnormalization(matched):
    return list(set(matched))


def indeal(config, content, title):
    devicekey = config["KEY_WORD"]
    if config["KEY_CHAR"] is not None and config["KEY_NUM"] is not None:
        devicekey = str(config["KEY_CHAR"][0:29])
        target = compilematch(config["KEY_CHAR"])
        begin, end = keynumsplit(config["KEY_NUM"])
       # print ("num,char", begin, end)
        all_c_match = match(target, content)
        part_c_match = match(target, content[begin:end])
        all_t_match = match(target, title)
        part_t_match = match(target, title[begin:end])
        if all_c_match == part_c_match:
            part_c_match = matchnormalization(part_c_match)
            return devicekey, part_c_match
        elif all_t_match == part_t_match:
            part_t_match = matchnormalization(part_t_match)
            return devicekey, part_t_match
        elif all_c_match != part_c_match:
            all_c_match = matchnormalization(all_c_match)
            return devicekey, all_c_match
        elif all_t_match != part_t_match:
            all_t_match = matchnormalization(all_t_match)
            return devicekey, all_t_match
        else:
            return devicekey, None
    elif config["KEY_CHAR"] is not None and config["KEY_NUM"] is None:
        devicekey = str(config["KEY_CHAR"][0:29])
        target = compilematch(config["KEY_CHAR"])
        all_c_match = match(target, content)
        all_t_match = match(target, title)
       # print  ("num", all_c_match, all_t_match)
        if all_c_match:
            all_c_match = matchnormalization(all_c_match)
            return devicekey, all_c_match
        elif all_t_match:
            all_t_match = matchnormalization(all_t_match)
            return devicekey, all_t_match
        else:
            return devicekey, None

    elif config["KEY_WORD"] is not None:
        devicekey = config["KEY_WORD"] 
        wordvalue_split_n = content.split(config["KEY_WORD"])[1].split("\n")[0].replace(":","").replace("：","").replace(" ","")
        wordvalue_split_ = content.split(config["KEY_WORD"])[1].split(" ")[0].replace(":","").replace("：","").replace(" ","")
        if wordvalue_split_n:
            return devicekey, wordvalue_split_n
        if wordvalue_split_:
            return devicekey, wordvalue_split_n
        return devicekey, None


    elif config["KEY_CHAR"] is None and config["KEY_NUM"] is not None:
        devicekey = config["KEY_NUM"]
        begin, end = keynumsplit(config["KEY_NUM"])
        part_c_match = content[begin:end]
        part_t_match = title[begin:end]
        if part_c_match:
            return devicekey, part_c_match
        elif part_t_match:
            return devicekey, part_t_match
        else:
            return devicekey, None

