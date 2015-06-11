# -*- coding: utf-8 -*-
from pydbg import *
from pydbg.defines import *
from fileformat import *
import windowhan  # 간단한 유틸 함수들 모음
import json
import utils
import random
import threading
import os
import shutil
import time

class file_fuzzer:
    def __init__(self, exe_path):
        self.mutate_count        = 30
        self.mutate_list         = []
        self.selected_list       = []
        self.eip_list            = [] 
        self.exe_path            = exe_path
        self.ext                 = ".avi"
        self.orig_file           = None
        self.sample_dir          = "sample\\"
        self.tmp_file            = None
        self.tmp_dir             = "tmp\\"
        self.count               = 0
        self.crash               = None
        self.crash_tracking      = False 
        self.crash_count         = None 
        self.tracking_count      = 0
        self.check               = False
        self.pid                 = None
        self.in_accessv_handler  = False
        self.dbg                 = None
        self.running             = False

    # 파일 선택
    def file_picker(self):
        file_list = os.listdir(self.sample_dir)
        self.tmp_file = self.tmp_dir+ "test.avi"
        self.orig_file = self.sample_dir+random.choice(file_list)
        time.sleep(2)
        shutil.copy(self.orig_file,  self.tmp_file)
        return

    def fuzz(self):

        while 1:

            while self.running :
                time.sleep(1)

            self.running = True

            print "[*] Starting debugger for iteration: %d" % self.count

            if self.crash_tracking == False:
                self.file_picker()
                self.mutate_file()
            else: 
                print "[+] Crash Tracking Start !!!", self.orig_file
                shutil.copy(self.orig_file, self.tmp_file)
                self.mutate_track()

            pydbg_thread = threading.Thread(target=self.start_debugger)
            pydbg_thread.setDaemon(0)
            pydbg_thread.start()

            while self.pid == None:
                time.sleep(0.5)

            monitor_thread = threading.Thread(target=self.monitor_debugger)
            monitor_thread.setDaemon(0)
            monitor_thread.start()

            self.count +=1


    def start_debugger(self):

        self.running = True
        self.dbg = pydbg()

        self.dbg.set_callback(EXCEPTION_ACCESS_VIOLATION,self.check_accessv)
        pid = self.dbg.load(self.exe_path, self.tmp_file)

        self.pid = self.dbg.pid
        self.dbg.run()


    def monitor_debugger(self):

        counter = 0
        print "[*] waiting ",
        while counter < 3 and self.pid != None:
            time.sleep(1)
            print ".",
            counter += 1
        print "\n"

        if self.in_accessv_handler != True:
            tid = c_ulong(0)
            if windll.kernel32.GetHandleInformation(self.dbg.h_process, byref(tid)) :
                self.dbg.terminate_process()
            self.dbg.close_handle(self.dbg.h_process)
            
        else:
            while self.pid != None:
                time.sleep(0.5)
        
        while True :
            try :
                os.remove(self.tmp_file)
                break
            except :
                time.sleep(0.2)

        self.in_accessv_handler = False
        self.running = False



    def check_accessv(self, dbg):
        if self.crash_tracking == False:
            
            if self.dbg.context.Eip in self.eip_list:
                print "\n[ + ] Duplicate Crash!!"
                self.in_accessv_handler = False
                self.dbg.terminate_process()
                self.pid = None

                return DBG_EXCEPTION_NOT_HANDLED

            self.eip_list.append(self.dbg.context.Eip)

            self.crash_tracking = True
            self.in_accessv_handler = True
            
            print "\n[*] Woot! Handling an access violation!"
            print "[*] EIP : 0x%08x" % self.dbg.context.Eip
            
            crash_bin = utils.crash_binning.crash_binning()
            crash_bin.record_crash(dbg)
            self.crash = crash_bin.crash_synopsis()

            # 크래시 일 때 카운트정보를 작성한다.
            self.crash_count = self.count
            # 크래시 정보 로깅
            now_date = time.strftime("%Y%m%d_%H:%M:%S")
            json_data = {}
            json_data["date"] = now_date
            json_data["count"] = self.count
            json_data["crash"] = self.crash
            json.dumps(json_data,ensure_ascii=False,encoding='utf-8')

            windowhan.postData("recoder.me",19904,"http://www.naver.com","http://recoder.me:19304/receive",json_data,None,"hojung browser")
            
            crash_fd = open("crash\\crash-%d.log" % self.count,"w")
            crash_fd.write(self.crash)
            crash_fd.write("----------------- mutate log -------------------\n")
            for i in self.mutate_list:
                crash_fd.write("offset : "+ hex(i[0])+", 0x"+i[1] + "\n" )
            crash_fd.close()

            # 원본 파일을 백업한다.
            shutil.copy(self.orig_file,"crash\\%d_orig%s" % (self.count,self.ext))

            self.dbg.terminate_process()
            self.pid = None

            return DBG_EXCEPTION_NOT_HANDLED


        else:
            
            self.in_accessv_handler = True
            self.dbg.terminate_process()
            self.pid = None
            
            print "[+] crash Again!!"
            self.mutate_list = self.selected_lis
            self.check = False

            print "[+] Mutate list count -- %d" % len(self.mutate_list)


            if len(self.mutate_list) == 1:
                print "[ ^^ ] tracking Finished! %d -> %d" % (self.mutate_count, len(self.mutate_list))
                
                shutil.copy(self.tmp_file, "crash\\crash_%d%s" % (self.crash_count,self.ext))

                
                f = open("crash\\crash_%d.log" % self.crash_count, 'a')
                f.write("\n\n---------------- Check this Offset!! ------------------\n\n")
                for i in self.mutate_list:
                    f.write("offset : "+ hex(i[0])+", 0x"+i[1] + "\n" )
                f.write("\n\nEND")
                f.close()

                self.crash_tracking = False
                self.crash_again = False
                self.crash_tracking_step = 0
                self.selected_list = []
                self.pivot = 0

            return DBG_EXCEPTION_NOT_HANDLED



    def mutate_file( self ):

        print "[*] Selected file : %s" % self.orig_file

        self.mutate_list = []
        fd = open(self.tmp_file, "r+b")
        stream = fd.read()
        stream_length = len(stream)
        attack = "A"
        format_data = FormatControl("avi",self.tmp_file).aviFormat()

        for i in range(0,random.randint(0,len(format_data)-1)):
            
            rand_offset = format_data[random.randint(0,len(format_data)-1)]
            rand_offset = rand_offset[rand_offset.keys()[random.randint(0,len(rand_offset.keys())-1)]]["startOffset"]
            mutate = attack * random.randint(1,4)
            print "[+] mutate offset : " + hex(rand_offset)
            self.mutate_list.append( (rand_offset, mutate.encode('hex')) )
            
            fd.seek(rand_offset)
            fd.write(mutate)

        fd.close()
        return

    def mutate_track( self ):
        self.tracking_count+=1
            
        pivot = len(self.mutate_list)/2


        if self.tracking_count > 20:
            print "[+] tracking Fail... "
            self.crash_tracking = False
            self.selected_list = []
            self.tracking_count = 0
            self.eip_list = []
            os.remove("crash\\%d_orig.avi" % self.crash_count)
            os.remove("crash\\crash-%d.log" % self.crash_count)
            return
        
        left = self.mutate_list[:pivot]
        right = self.mutate_list[pivot:]

        if self.check == False:
            print "left"
            self.selected_list = left
            self.check = True
        else:
            print "right"
            self.selected_list = right
            self.check = False
            
        f = open(self.tmp_file, 'r+b')
        
        for i in self.selected_list:
            #print i[0], i[1]
            f.seek(i[0])
            f.write(chr(int(i[1][:2],16)) * (len(i[1])/2))
        f.close()


        
        return

if __name__ == "__main__":

    print "[*] File Fuzzer."
    exe_path = "C:\\Program Files\\TokApps\\TokPlayer\\TokPlayer.exe"
    
    fuzzer = file_fuzzer( exe_path)
    fuzzer.fuzz()
