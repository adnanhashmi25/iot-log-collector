import sys
from PLD_AGENT import Agent as nms
import csv
import os
from collections import defaultdict as df
import multiprocessing
import time
current_directory = os.path.dirname(os.path.realpath(__file__))
lsmname = sys.argv[1]

#print(current_directory)
#users = [('su - samsung','S@m$uNg$0503@'),('su -','S@msung1te')]


def read_user_file(file_name):
    users = set()
    with open(file_name) as f:
        for line in f.readlines():
            if line:
                users.add((line.split(',')[0].strip(),line.split(',')[1].strip()))

    return list(users)   
        

def main(x):
    host_name, host_ip, cmds,path,users = x
    n = nms(host_name, host_ip, cmds, users)
    print("Execution  start on "+host_name)
    with open(path+'/'+host_name+'.csv','wb') as status_file:
    	fw = csv.writer(status_file)
    	fw.writerow(['LSM_NAME','SAP_ID','eNB_down_or_pwd_not_ok','Root_Authentication_Fail','CMD','Status'])
   
    
    	with open(path+'/'+host_name+'.txt','wb') as fl:
        	try:
            		node_status = n.connect()
            		if node_status:
                		eNB_down_or_pwd_not_ok = "No"
            		else:
                		eNB_down_or_pwd_not_ok = "Yes"
                
        	except Exception, e:
            		print "can't connect to ", host_name
            		print e
            		fl.write("can't connect to "+ host_name+"\r\n")
            		eNB_down_or_pwd_not_ok = "Yes"

        	try:
            		root_status = n.connect_root()
            		if root_status:
                		root_auth = 'No'
            		else:
                		root_auth = 'Yes'
        	except:
            		print "can't connect to root ", host_name
            		fl.write("can't connect to root "+ host_name+"\r\n")
            		root_auth = 'Yes'

        
        
        	if root_status:
            		#cmds.extend(['cd /var/log/OAM/DB','ls -ltr|grep pldx'])
            		for cmd in cmds:
                		if 'input' in cmd:
                    			for cmd in [cmd, cmd.split('=')[0].strip().replace('input', 'output')+';']:
                        			status = n.run_command(cmd,['root@'],150)

                        			if status:
                            				#print "execute successfully", host_name, cmd
                            				fl.write("execute successfully "+host_name+" "+cmd+"\r\n")
                            				fw.writerow([lsmname,host_name,eNB_down_or_pwd_not_ok,root_auth,cmd,"Executed"])
                        			else:
                            				#print "not execute", host_name, cmd
                            				fl.write("not execute "+host_name+" "+cmd+"\r\n")
                            				fw.writerow([lsmname,host_name,eNB_down_or_pwd_not_ok,root_auth,cmd,"Not Executed"])
                    
                		else:
		    			timer_1 = time.time()
                    			status = n.run_command(cmd, ['root@'],150)
		    			if (float(time.time())-float(timer_1))>=150:
						fl.write("took more time to respond "+host_name+" "+cmd+"\r\n")
                				fw.writerow([lsmname,host_name,eNB_down_or_pwd_not_ok,root_auth,cmd,"High Latency"])
						return
		

                    			elif status:
                        			#print "execute successfully", host_name, cmd
                        			fl.write("execute successfully "+host_name+" "+cmd+"\r\n")
                        			fw.writerow([lsmname,host_name,eNB_down_or_pwd_not_ok,root_auth,cmd,"Executed"])
                    			else:
                        			#print "not execute", host_name, cmd
                        			fl.write("not execute "+host_name+" "+cmd+"\r\n")
                        			fw.writerow([lsmname,host_name,eNB_down_or_pwd_not_ok,root_auth,cmd,"Not Executed"])
            

                        
        	else:
            		for cmd in cmds:
                		#print "root Authentication failure", host_name, cmd
                		fl.write("root Authentication failure"+host_name+" "+cmd+"\r\n")
                		fw.writerow([lsmname,host_name,eNB_down_or_pwd_not_ok,root_auth,cmd,"Not Executed"])
                
               
	n.close()
        
        

if __name__ == "__main__":

    users = read_user_file(current_directory+"/users.txt")
    f = open(current_directory+"/Input.csv", "rb")
    fc = csv.reader(f)
    #fl = open(current_directory+'/status.txt', 'wb')
    sites = df(list)
    for row in fc:
        if len(row) < 2:continue
        sites['|'.join(row[0:2])].append(row[2])
        
    f.close()
    if len(sites)>=10:    
        pool = multiprocessing.Pool(10)
    else:
        pool = multiprocessing.Pool(len(sites))
        
    pool.map(main, [(key.split('|')[0], key.split('|')[1], value, current_directory+'/STATUS', users) for key, value in sites.items()])
    pool.close()
    
    #fl.close()
    
