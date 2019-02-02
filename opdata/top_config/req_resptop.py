#!/usr/bin/env python

import hashlib
import time
import requests
from .url import config_url


class reqtop_ready:
    def config_data(self, email):
        data = {}
        clientSubmitTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        key_ = "clientSubmitTime="+clientSubmitTime+"itsMonitorMd5key"
        secret = hashlib.md5()
        secret.update(key_.encode(encoding="utf-8"))
        data.update({"key": secret.hexdigest()})
        data.update({"email": email})
        data.update({"clientSubmitTime": clientSubmitTime})
        r = requests.post(config_url, json=data)
        return r.text
