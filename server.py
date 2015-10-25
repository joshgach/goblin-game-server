import dpkt
import socket, random, re, os
import time
from scapy.all import *

ghealth = 100 #Sets the health of the regular goblin
mhealth = 200 #Sets the health of the master goblin

def move(action):
    #Creates the ICMP Packet to send
    echo = dpkt.icmp.ICMP.Echo()
    echo.id = random.randint(0, 0xffff)
    echo.seq = random.randint(0, 0xffff)
    icmp = dpkt.icmp.ICMP()
    icmp.type = dpkt.icmp.ICMP_ECHO
    icmp.data = echo
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, dpkt.ip.IP_PROTO_ICMP)
    s.connect(('172.16.12.1', 1)) #Specifies the IP Address to which the ICMP packet is sent
    #timeout = timer.start()
    #if (timeout = 10):
    i = random.randint(0,10)
    action = action.lower()
    if (action == 'g-attack'):
        if (i <= 8):
            echo.data = 'G-Attack' #Goblin does a regular attack
            sent = s.send(str(icmp))
        else:
            echo.data = 'G-Attack-Crit' #Goblin gets a critical hit with its regular attack
            sent = s.send(str(icmp))
    elif (action == 'g-defend'):
        echo.data = 'G-Defend' #Goblin defends itself
        sent = s.send(str(icmp))
    elif (action == 'g-f-ball'):
        if (i <= 8):
            echo.data = 'G-F-Ball' #Goblin uses a fireball
            sent = s.send(str(icmp))
        else:
            echo.data = 'G-F-Ball-Crit' #Goblin gets a critical hit with the fireball
            sent = s.send(str(icmp))

def captureICMP(pkt): #Capture packets sent from the client
    global ghealth #Imports the global health variable
    raw = pkt.sprintf('%Raw.load%')# grabs the data portion of the ICMP packet
    if raw == "'Attack'": #Player attack incomming
        move = re.findall('Attack', raw)
        ghealth = ghealth - 25
        print move[0]
    elif raw == "'Attack-Crit'": #Player attack incomming thats critical
        move = re.findall('Attack-Crit', raw)
        ghealth = ghealth - 50
        print move[0]
    elif raw == "'Defend'": #Player is defending
        move = re.findall('Defend', raw)
        print move[0]
    elif raw == "'F-Ball'": #Player fireball incomming
        move = re.findall('F-Ball', raw)
        print move[0]
        ghealth = ghealth - 30
    elif raw == "'F-Ball-Crit'": #Player fireball incomming thats critical
        move = re.findall('F-Ball-Crit', raw)
        ghealth - ghealth - 60
        print move[0]

def main():    
    attacks = ['g-attack', 'g-defend', 'g-f-ball']
    conf.iface = 'eth1' #Tells scapy what interface to monitor
    while (ghealth >= 0):
        i = random.randint(0,2)
        move(attacks[i]) #Randomize what moves will be used
        print attacks[i]
        sniff(filter='icmp', prn=captureICMP, count=1, timeout = 10) #Sniffs for ICMP packets while waiting for either 1 packet of a 10 second timeout
    print 'Goblin is dead'

if __name__ == '__main__':
    main()
