#!/usr/bin/python3
####################################################################
# CG Lamitie
# ethtool_test.py
#
# using ethtool to test link status
#  
####################################################################

#nicArray=(ip -f link a | awk '$1 ~ /[0-9]/ { print $2 }' |  sed 's/://g')
#import array as nicArray

## [playing with subprocess and ip command]
#import subprocess
#p = subprocess.Popen("ip -f link a", stdout=subprocess.PIPE, shell=True)
#(output, err) = p.communicate()
#p_status = p.wait()
#print("Command output :\n", output.decode())
#print("Command exit status/return code : ", p_status)
## [done playing with subprocess and ip command]

## plyaing with socket to get intrface names
#import socket
##socket.if_nameindex()
#for interfaces in socket.if_nameindex():
#    interface_name = interfaces[1]
#    print(interface_name)
## done playing with socket to get interface names


## ChatGPT generated code off the following prompt:
## "Write a Linux python script using socket to display all interfaces and state which interfaces are up"
import socket
import fcntl
import struct

def get_interface_status(interface_name):
    SIOCGIFFLAGS = 0x8913
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ifreq = struct.pack('16sH14s', interface_name.encode('utf-8'), 0, b'\x00' * 14)
    try:
        res = fcntl.ioctl(sock.fileno(), SIOCGIFFLAGS, ifreq)
        flags = struct.unpack('16sH14s', res)[1]
        return flags & 1 == 1  # Check if IFF_UP bit is set
    except IOError:
        return False

def get_all_interfaces():
    interfaces = []
    with open('/proc/net/dev', 'r') as f:
        lines = f.readlines()[2:]  # Skip header lines
        for line in lines:
            interface = line.split(':')[0].strip()
            interfaces.append(interface)
    return interfaces

all_interfaces = get_all_interfaces()
print("All interfaces:")
for interface in all_interfaces:
    status = "UP" if get_interface_status(interface) else "DOWN"
    print(f"{interface}: {status}")
    

