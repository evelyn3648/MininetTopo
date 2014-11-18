#!/usr/bin/env python
import re
import os
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.topo import Topo

host = {}
switch = {}
net = Mininet( topo=None, build=False, link=TCLink)

def myNetwork():
    info( '*** Adding controller\n' )
    net.addController(name='c0', controller=RemoteController, ip='X.X.X.X')
    depth=3
    building=4
    fanout=2
    switches = {} 
    hosts = []
    switches[0] = list()

    #building core switch
    for b in range(0,building):
        print 1+b*((fanout**depth-1)/(fanout-1))
        switches[0].append(net.addSwitch('s%s'%(1+b*((fanout**depth-1)/(fanout-1)))))

    #switches
    for s in range(1, depth):
	switches[s] = list()
        for b in range(0,building):
	    for sw in range(0,fanout**s):
	        switch_id = fanout**s+sw+b*((fanout**depth-1)/(fanout-1))
	        switches[s].append(net.addSwitch('s%s'%(switch_id)))
                net.addLink(switches[s][-1],switches[s-1][(sw//fanout)+b*s])

    #hosts
    for h in range(0, fanout**depth*building):
        hosts.append(net.addHost('h%s'%(h+1),ip='192.168.%s.%s/24'%((h//fanout**depth),(str(200+((h+1)%fanout**depth)))))) 
        net.addLink(hosts[-1],switches[depth-1][(h//fanout)])
   
    Gateway = net.addHost('Gateway',ip='192.168.0.254/24')
    for b in range(0,building):
        net.addLink(Gateway,switches[0][b])

    net.start()
    Gateway.cmdPrint('ifconfig Gateway-eth1 192.168.1.254')
    Gateway.cmdPrint('ifconfig Gateway-eth2 192.168.2.254')
    Gateway.cmdPrint('ifconfig Gateway-eth3 192.168.3.254')
    Gateway.cmdPrint('echo "1" > /proc/sys/net/ipv4/ip_forward')
    for h in range(0, fanout**depth*building):
        hosts[h].cmdPrint('route add default gw 192.168.%s.254 %s'%((h//fanout**depth),(str(hosts[h].defaultIntf().name))))


    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
