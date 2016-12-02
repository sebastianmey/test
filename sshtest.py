#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mi Okt 21 18:51:50 2015

@author:    Sebastian Mey, Institut für Kernphysik, Forschungszentrum Jülich GmbH            
            s.mey@fz-juelich.de
"""
import os, paramiko, sys
from scp import SCPClient

    
def main(argv):
    sshIP = "snoopy.cc.kfa-juelich.de"
    sshUser = "cosy"
    sshPWD = "rin.ran"
    ifile =  "/mnt/cc-x/smb/fsv/update"

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    try:
        ssh.connect(hostname = sshIP, username = sshUser, password = sshPWD, look_for_keys = False, allow_agent = False)
        print("Connected to %s@%s via SSH." %(sshUser, sshIP))
    except (paramiko.AuthenticationException, paramiko.SSHException) as err:
        print("Could not connect to %s@%s: %s" %(sshUser, sshIP, err))
        sys.exit(2)
    scp = SCPClient(ssh.get_transport())
    try:
        scp.get(ifile)
        print("File %s copied to ." %ifile)
        ssh.close()
    except:
        print("Could not find %s." % ifile)
        ssh.close()  
        sys.exit(2)

                    
if __name__ == "__main__":
    main(sys.argv[1:])
