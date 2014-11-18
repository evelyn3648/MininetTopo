#!/usr/bin/env python2                                                                       
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.node import Controller, RemoteController
from mininet.cli import CLI 
from mininet.link import Intf
from mininet.util import dumpNodeConnections
import os
import shutil


REMOTE_CONTROLLER_IP="127.0.0.1"

def MininetTopo():
    '''
    Prepare Your Topology
    '''
    net = Mininet (topo=None, build=False)

    controller = net.addController(name='controller0', controller=RemoteController, ip=REMOTE_CONTROLLER_IP, port=6633)

    info("Create Host node\n")
    host1 = net.addHost('h1', ip='10.0.0.1')
    host2 = net.addHost('h2', ip='10.0.0.2')
    web1 = net.addHost('web1', ip='10.0.0.3', mac='00:00:00:00:00:01')
    web2 = net.addHost('web2', ip='10.0.0.4', mac='00:00:00:00:00:02')
    web3 = net.addHost('web3', ip='10.0.0.5', mac='00:00:00:00:00:03')
    info("Create Switch node\n")
    switch = net.addSwitch('s1')

    info("Link switch to host\n")
    net.addLink(switch, host1)
    net.addLink(switch, host2)
    net.addLink(switch, web1)
    net.addLink(switch, web2)
    net.addLink(switch, web3)

    '''
    Working your topology
    '''
    info("Start network\n")
    net.start()
    info("Dumping host connections\n")
    dumpNodeConnections(net.hosts)

    info("Testing network connectivity\n")
    net.pingAll()

    info("Build web server\n")
    web1.cmdPrint('cd ~/mininet_web/web1/ && python2 -m SimpleHTTPServer 80 >& ~/mininet_web/web1/http-web1.log &')
    web2.cmdPrint('cd ~/mininet_web/web2/ && python2 -m SimpleHTTPServer 80 >& ~/mininet_web/web2/http-web2.log &')
    web3.cmdPrint('cd ~/mininet_web/web3/ && python2 -m SimpleHTTPServer 80 >& ~/mininet_web/web3/http-web3.log &')

    info("Help yourself\n")
    info("Try it: h1 wget -O - 10.0.0.3\n")
    CLI(net)


    '''
    Clean mininet
    '''
    web1.cmdPrint('kill %python')
    web2.cmdPrint('kill %python')
    web3.cmdPrint('kill %python')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    MininetTopo()
