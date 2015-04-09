#!/usr/bin/env python

import os
import time
import re

class UTS800(object):
    #class MHLTYPE(object):
    #    MHL2 = "MHL2"
    #    MHL3 = "MHL3"
    #
    #@classmethod
    #def new_mhl(cls, **kwargs):
    #    mhl_type = kwargs.pop("type").upper()
    #    if mhl_type == UTS800.MHLTYPE.MHL2:
    #        return mhl2(**kwargs)
    #    elif mhl_type == UTS800.MHLTYPE.MHL3:
    #        return mhl3(**kwargs)
    #    else:
    #        raise ValueError("Unsupported MHL type: %s" % mhl_type)

    class MHLTYPE(object):
        MHL2_EXPLORER = "MHL2_EXPLORER"
        MHL2_ANALYZER = "MHL2_ANALYZER"
        MHL3 = "MHL3"
    
    @classmethod
    def new_mhl(cls, **kwargs):
        mhl_type = kwargs.pop("type").upper()
        if mhl_type == UTS800.MHLTYPE.MHL2_EXPLORER:
            return mhl2_explorer(**kwargs)
        elif mhl_type == UTS800.MHLTYPE.MHL2_ANALYZER:
            return mhl2_analyzer(**kwargs)
        elif mhl_type == UTS800.MHLTYPE.MHL3:
            return mhl3(**kwargs)
        else:
            raise ValueError("Unsupported MHL type: %s" % mhl_type)
        
class mhl2_explorer(object):
    def __init__(self,cdf_path):
        self.cdf_path = cdf_path

    def test_mhl2_explorer(self):
        # the test case numbers depends on cdf_file, so each DUT 
        exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mhl2_cts_explorer", "CBusConsole.exe")
        cmd = exe_path +" "+self.cdf_path
        f = open("run.bat",'w')
        f.write('cd\\\n')
        f.write('cd C:\husky\lib\simg\util\uts800\mhl2_cts_explorer\n')
        f.write(exe_path +" "+self.cdf_path+ ' \n')
        f.close()
        time.sleep(3)
        res = os.system("run.bat")
        print str(res)
        if res == 0:
            return res
        else:
            return -1
        
class mhl2_analyzer(object):
    def __init__(self,device_type):
        self.device_type = device_type

        
    #def test_mhl2_analyzer(self,test_id="-1",operand0="-1",operand1="-1",operand2="-1",operand3="-1",operand4="-1"):
    def test_mhl2_analyzer(self,cmd,checklog=False):        
        exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mhl2_cts_analyzer", "MHLRxTxConsole1.2.2.exe")
        print ("=========================")
        print(exe_path+" "+self.device_type+" "+cmd)
        
        res = -1
        if checklog == False:
            res = os.system(exe_path+" "+self.device_type+" "+cmd)
        else:
            path = os.path.dirname(exe_path)
            os.system("del " +path+"\\Log*.log")
            res1 = os.system(exe_path+" "+self.device_type+" "+cmd)
            res2 = 0
            temp_log = ""
            for filename in os.listdir(path):
                if re.search(".log",filename,re.I):
                    temp_log = filename
            f = open(path+"\\"+ temp_log,'r')
            lines = f.readlines()
            for line in lines:
                if re.search("fail",line,re.I):
                    res2 = -1
                    break
            f.close
            if res1 == 0 and res2 ==0:
                res = 0
            
        print str(res)
        
        if res == 0:
            return res
        else:
            return -1


class mhl3(object):
    def __init__(self,cdf_path,test_list):
        self.cdf_path = cdf_path
        self.test_list = test_list
        
    def test_mhl3_automation(self):
        exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mhl3_cts_automation", "TestApplicationCMD.exe")
        result = os.path.dirname(self.cdf_path)+ "\\result.txt"
        #print "result =" + result
        cmd = exe_path +" "+self.cdf_path +" " +self.test_list + " >" +result
        res = os.system(cmd)
        time.sleep(3)
        f = open(result,'r')
        lines = f.readlines()
        actual_result = "FAIL"
        for line in lines:
            line = line.strip()
            if line:
                print line
            if re.search("----Result: Pass",line,re.I):
                actual_result = "PASS"
                break
        f.close
        return actual_result



    def test_mhl3_manual(self):
        pass

        
if __name__ == "__main__":
    cts = mhl3(r"C:\husky\lib\simg\util\uts800\CDF_Rogue_Sink.ini",r"C:\husky\lib\simg\util\uts800\6_3.xml")
    cts.test_mhl3_automation()
