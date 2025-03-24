from pexpect import pexpect
import time
import re
import os
import signal
current_directory = os.path.dirname(os.path.realpath(__file__))
class Agent(object):

    def __init__(self,host, enb_ip,cellnums,users):
        self.enb_ip = enb_ip
        self.host =host 
        self.session = None
        self.layer = -1
        self.prompt = None
        self.cellnums = cellnums
        self.users = users

    def connect(self,):
        try:
            self.session = pexpect.spawn("ssh -o UserKnownHostsFile=/dev/null\
            -o StrictHostKeyChecking=no lteuser@"+self.enb_ip)
            self.log = open(current_directory+"/LOGS/"+self.host, 'wb')
            self.log.write("="*10+self.host+","+self.enb_ip+"="*10+"\r\n")
            if self.session:
                self.session.logfile = self.log
                self.session.expect("assword")
                self.session.sendline("samsunglte")
                self.session.expect("lteuser")
                self.layer+=1
                return True
            else:
                return False
        except:
            return False

##    def connect_root(self, pas):
##        self.session.sendline('su - samsung')
##        index = self.session.expect(['assword', pexpect.EOF, pexpect.TIMEOUT],
##                                    timeout=10)
##        if index == 0:
##            self.session.sendline(pas)
##            index_1 = self.session.expect(['root', pexpect.EOF, pexpect.TIMEOUT],
##                                     timeout=10)
##            if index_1 == 0:
##                self.layer+=1
##                return True
##            else:
##                return False
##        else:
##            return False

    def connect_root(self,):
        for user_id,pas in self.users:
            try:
            	self.session.sendline(user_id)
            	index = self.session.expect(['assword', pexpect.EOF, pexpect.TIMEOUT],
                                        timeout=10)
            	if index == 0:
                     self.session.sendline(pas)
                     index_1 = self.session.expect(['root', pexpect.EOF, pexpect.TIMEOUT],
                                         timeout=10)
                     if index_1 == 0:
                    	self.layer+=1
                    	return True
                     else:
                        if (user_id,pas) == self.users[-1]:
                            return False
                        else:
                            continue
            except Exception as e:
            	continue
            
        return False

            
                                  
            
    def run_command(self, cmd, prompt, timeinsec):
        self.session.sendline(cmd)
        if type(prompt) == list:
            prompt.append(pexpect.EOF)
            prompt.append(pexpect.TIMEOUT)
            index = self.session.expect(prompt, timeout = timeinsec)
        else:
            index = self.session.expect([prompt, pexpect.EOF, pexpect.TIMEOUT], timeout = timeinsec)
        if index != -1:
            return self.session.before
        else:
            return False

    def close(self,):
        for i in range(self.layer):
            self.session.sendline('exit')
            time.sleep(0.1)
        #self.session.close()
        self.session.kill(signal.SIGKILL)
	self.log.close()
