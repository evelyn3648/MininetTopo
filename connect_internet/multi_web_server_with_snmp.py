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
TEST_DIR_PATH="/tmp/"

def MininetTopo():
    '''
    Prepare Your Topology
    '''
    net = Mininet (topo=None, build=False)

    controller = net.addController(name='controller0', controller=RemoteController, ip=REMOTE_CONTROLLER_IP, port=6633)

    info("Create Host node\n")
    host1 = net.addHost('h1', ip='192.168.71.220/24')
    web1 = net.addHost('web1', ip='192.168.71.221/24', mac='00:00:00:00:00:01')
    web2 = net.addHost('web2', ip='192.168.71.222/24', mac='00:00:00:00:00:02')
    web3 = net.addHost('web3', ip='192.168.71.223/24', mac='00:00:00:00:00:03')
    info("Create Switch node\n")
    switch = net.addSwitch('s1')

    info("Link switch to host\n")
    net.addLink(switch, host1)
    net.addLink(switch, web1)
    net.addLink(switch, web2)
    net.addLink(switch, web3)

    '''
    Working your topology
    '''
    info("Start network\n")
    net.start()
    os.popen("ovs-vsctl add-port s1 eth0")
    os.popen("ifconfig eth0 0")
    os.popen("ip route del 0/0")
    os.popen("ifconfig s1 192.168.71.219")
    os.popen("ip route add 0/0 via 192.168.71.2 dev s1")
    os.popen("ovs-vsctl set-fail-mode s1 secure")
    host1.cmdPrint('route add default gw 192.168.71.2')
    web1.cmdPrint('route add default gw 192.168.71.2')
    web2.cmdPrint('route add default gw 192.168.71.2')
    web3.cmdPrint('route add default gw 192.168.71.2')
    info("Dumping host connections\n")
    dumpNodeConnections(net.hosts)

#    info("Testing network connectivity\n")
#    net.pingAll()

    info("Build web server\n")
    web1.cmdPrint('cd ~/mininet_web/web1/ && python2 -m SimpleHTTPServer 80 >& ~/mininet_web/web1/http-web1.log &')
    web1.cmdPrint('/usr/sbin/snmpd -LS n d -Lf /dev/null -p /var/run/snmpd.pid')
    web2.cmdPrint('cd ~/mininet_web/web2/ && python2 -m SimpleHTTPServer 80 >& ~/mininet_web/web2/http-web2.log &')
    web2.cmdPrint('/usr/sbin/snmpd -LS n d -Lf /dev/null -p /var/run/snmpd.pid')
    web3.cmdPrint('cd ~/mininet_web/web3/ && python2 -m SimpleHTTPServer 80 >& ~/mininet_web/web3/http-web3.log &')
    web3.cmdPrint('/usr/sbin/snmpd -LS n d -Lf /dev/null -p /var/run/snmpd.pid')

    info("Help yourself\n")
    info("Try it: h1 wget -O - <web_server_IP>\n")
    info("Test SNMP function")
    web1.cmdPrint('snmpwalk -v 2c -c public localhost system')
    web2.cmdPrint('snmpwalk -v 2c -c public localhost system')
    web3.cmdPrint('snmpwalk -v 2c -c public localhost system')
    CLI(net)


    '''
    Clean mininet
    '''
    web1.cmdPrint('kill %python')
    web2.cmdPrint('kill %python')
    web3.cmdPrint('kill %python')
    net.stop()
    os.popen("sh ~/mininet/examples/Load_balance/disconnect.sh")


if __name__ == '__main__':
    setLogLevel('info')
    MininetTopo()
