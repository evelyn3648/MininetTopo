ovs-vsctl del-port s1 eth0
ifconfig s1 0
ip route del 0/0
ifconfig eth0 192.168.71.219
ip route add 0/0 via 192.168.71.2 dev eth0
