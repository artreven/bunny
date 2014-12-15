'''
Created on Dec 15, 2014

@author: artreven
'''
import rfoo
import subprocess
import os

class MyHandler(rfoo.BaseHandler):
    def RPopen(self, call_str):
        with open(os.devnull, "w") as fnull:
            ans = subprocess.call(call_str, shell=True, stdout=fnull, stderr=fnull)
        return ans

rfoo.UnixServer(MyHandler).start('P9M4')