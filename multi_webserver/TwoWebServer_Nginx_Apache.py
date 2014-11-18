import re
import os
from mininet.util import quietRun
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info,error
from mininet.node import Controller, RemoteController, OVSKernelSwitch
def myNetwork():
    OVSKernelSwitch.setup()
    net = Mininet( topo=None, controller=lambda name: RemoteController( name, ip='192.168.56.110' ) )
    info( '*** Adding controller\n' )
    net.addController(name='c0')

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1')
    h1 = net.addHost('server1',ip='10.0.0.1')
    h2 = net.addHost('server2',ip='10.0.0.2')
    h3 = net.addHost('server3',ip='10.0.0.3')
    client = net.addHost('client',ip='10.0.0.4')

    info( '*** Add links\n')
    net.addLink(s1,h1)
    net.addLink(s1,h2)
    net.addLink(s1,h3)
    net.addLink(s1,client)
    info( '*** Starting network\n')
    net.start()
    h1.cmdPrint('/etc/init.d/apache2 restart')
    h2.cmdPrint('/etc/init.d/nginx restart')
    client.cmdPrint('firefox')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
