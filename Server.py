import csv
import paramiko
import time
import fnmatch

class Server(object):

    def __init__(self, lsm_name, lsm_ip):
        self.lsm_name = lsm_name
        self.lsm_ip = lsm_ip
        self.ssh = None
        self.ftp = None
        self.remote_folder = str(time.time()).replace('.', '_')
        self.remote_file = None

    def connect(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.lsm_ip, username='user', password='password')
        except:
            print ("Can't connect to {0}".format(self.lsm_name))
            return False
        return True

    def upload_code_file(self, local_file, remote_file):
        self.ftp = self.ssh.open_sftp()
        self.remote_file = remote_file
        try:
            self.ftp.put(local_file, remote_file)
        except:
            print ("Can't execute on {0}".format(self.lsm_name))
            return False
        return True

    def extract_remote_code(self, remote_file_path, remote_file_folder):
        #print(remote_file_path)
        #print(remote_file_folder)
        stdin, stdout, stderr = self.ssh.exec_command('(unzip {0} ) && (mv PLD {1})'.format(remote_file_path, remote_file_folder + self.remote_folder))
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            print ("Can't Execute on {0}".format(self.lsm_name))
            return None
        self.remote_folder = remote_file_folder + self.remote_folder
        return self.remote_folder

    def upload_input_file(self, local_input_file, remote_file_name):
        try:
            remote_file_name = self.remote_folder + '/' + remote_file_name
            self.ftp.put(local_input_file, remote_file_name)
        except:
            print("Can't execute on {0}".format(lsm_name))
            return None
        return remote_file_name

    def get_remote_folder(self):
        return self.remote_folder

    def get_remote_file(self):
        return self.remote_file

    def run(self, launch_script, remote_path):
        stdin, stdout, stderr = self.ssh.exec_command('chmod 775 {0}/{1}'.format(remote_path, launch_script))
        stdin, stdout, stderr = self.ssh.exec_command('python {0}/{1} {2}'.format(remote_path, launch_script,self.lsm_name))
        print('Running on {0}'.format(self.lsm_name))
        l = list()
        for i in stdout:
            print(i)
            l.append(i)
        exit_status = stdout.channel.recv_exit_status()
        print(exit_status)
        if exit_status != 0:
            print("Couldn't Execute on {0}".format(self.lsm_name))
            print(stderr.readlines())
            print(stdout.readlines())
            return None
        else:
            return l

    def download(self, directory_list):
        print(directory_list)
        for directory,destination in directory_list:
            print('downloading from', directory)
            files = self.ftp.listdir(path=directory)
            for fl in files:
                self.ftp.get(directory + '/' + fl, destination.strip()+'{0}_{1}'.format(self.lsm_name, fl))
        return True
    
    
    def close_and_clean(self, remote_directory):
        try:
            stdin, stdout, stderr = self.ssh.exec_command('rm -rf {0}'.format(remote_directory))
            self.ftp.remove(self.remote_file)
        except Exception as e:
            print(e, self.lsm_name)
        finally:
            try:
                self.ftp.close()
                self.ssh.close()
            except:
                pass
        return True
