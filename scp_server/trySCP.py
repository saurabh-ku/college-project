import os
import paramiko
from scp import SCPClient

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

ssh = createSSHClient("192.168.43.70", 22, "pi", "raspberry")
scp = SCPClient(ssh.get_transport())
scp.get("/home/pi/Documents/college-project/data", "./fromscp", recursive = True)
