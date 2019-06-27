#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.log import info
from mininet.util import pmonitor
from mininet.cli import CLI
from mininet.node import Node
#from mininet.nodelib import LinuxBridge
from time import time
from time import sleep


#bottleneck bandwith = 400 mbps
#bottleneck buffer = 2Mbyte
#RTT varia entre 16ms e 324ms
#2 fluxos com mesmo RTT

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class MyTopo( Topo ):
    
    def build( self, **_opts ):

        defaultIP1 = '10.0.5.1/24' #IP pro roteador 1
        
        #s1 = self.addSwitch( 's1', cls=LinuxBridge)

        router1 = self.addNode( 'r1', cls=LinuxRouter, ip=defaultIP1, defaultRoute='via 10.0.6.2')
        

        client1 = self.addHost( 'h1', ip='10.0.5.10/24', defaultRoute='via 10.0.5.1')
        client2 = self.addHost( 'h2', ip='10.0.4.10/24', defaultRoute='via 10.0.4.1' )
        client3 = self.addHost( 'h3', ip='10.0.3.10/24', defaultRoute='via 10.0.3.1' )
        client4 = self.addHost( 'h4', ip='10.0.2.10/24', defaultRoute='via 10.0.2.1' )

        self.addLink(client1, router1, intfName2='r1-eth1', params2={ 'ip': '10.0.5.1/24'} )
        self.addLink(client2, router1, intfName2='r1-eth2', params2={ 'ip': '10.0.4.1/24'})
        self.addLink(client3, router1, intfName2='r1-eth3', params2={ 'ip': '10.0.3.1/24'})
        self.addLink(client4, router1, intfName2='r1-eth4', params2={ 'ip': '10.0.2.1/24'})
        


        


        defaultIP2 = '10.0.6.2/24' #IP pro roteador 2
        router2 = self.addNode( 'r2', cls=LinuxRouter, ip=defaultIP2, defaultRoute='via 10.0.6.1')
        self.addLink(router2, router1, intfName2='r1-eth5', params2={'ip':'10.0.6.1/24'})
        #,intfName2='r2-eth1', params2={'ip':defaultIP2}

        server1 = self.addHost( 'server1', ip='10.0.10.100/24', defaultRoute='via 10.0.10.1' )
        server2 = self.addHost( 'server2', ip='10.0.9.110/24', defaultRoute='via 10.0.9.1' )
        server3 = self.addHost( 'server3', ip='10.0.8.130/24', defaultRoute='via 10.0.8.1' )
        server4 = self.addHost( 'server4', ip='10.0.7.140/24', defaultRoute='via 10.0.7.1')
       
        self.addLink(server1, router2, intfName2='r2-eth1', params2={ 'ip': '10.0.10.1/24'} )
        self.addLink(server2, router2, intfName2='r2-eth2', params2={ 'ip': '10.0.9.1/24'} )
        self.addLink(server3, router2, intfName2='r2-eth3', params2={ 'ip': '10.0.8.1/24'} )
        self.addLink(server4, router2, intfName2='r2-eth4', params2={ 'ip': '10.0.7.1/24'} )

        # Each host gets 50%/n of system CPU
        #host = self.addHost( 'h%s' % (h + 1), cpu=.5/n )
        # 10 Mbps, 5ms delay, 2% loss, 1000 packet queue
        #self.addLink( host, switch, bw=400, delay='8ms', loss=2, max_queue_size=1000, use_htb=True )

def perfTest():
    "Test linux router"
    topo = MyTopo()
    net = Mininet( topo=topo )  # controller is used by s1-s3

    net.start()

   
    # net['h1'].cmdPrint('tc qdisc change dev h1-eth0 root netem delay 162ms 162ms distribution normal')
    # net['h2'].cmdPrint('tc qdisc change dev h2-eth0 root netem delay 164ms 16ms distribution normal')

    # info('Testando com o reno:\n')
    # net['server1'].cmdPrint('iperf -s -Z reno -i 1> resultReno1 &')
    # net['server2'].cmdPrint('iperf -s -Z reno -i 1 > resultReno2 &')
    
    
    # sleep(4)
    # net['h1'].cmdPrint('iperf -c 10.0.10.100 -Z reno -t 30 ')
    # net['h2'].cmdPrint('iperf -c 10.0.9.110 -Z reno -t 30 ')

    # # net['h1'].cmdPrint('tc qdisc change dev penis root netem delay 162ms 162ms distribution normal')
    # # net['h2'].cmdPrint('tc qdisc change dev h2-eth0 root netem delay 164ms 16ms distribution normal')
    
    # info('Testando com o cubic:\n')
    # net['h1'].cmdPrint('sudo /sbin/modprobe tcp_cubic')
    # net['h2'].cmdPrint('sudo /sbin/modprobe tcp_cubic')
    # net['server1'].cmdPrint('iperf -s -Z cubic -i 1 > resultCubic1 &')
    # net['server2'].cmdPrint('iperf -s -Z cubic -i 1 > resultCubic2 &')
    # sleep(4)
    # net['h1'].cmdPrint('iperf -c 10.0.10.100 -Z cubic -t 30 &')
    # net['h2'].cmdPrint('iperf -c 10.0.9.110 -Z cubic -t 30 &')
    #cat resultReno1 | grep sec | head -15 | tr - " " | awk '{print $4, $8}' > newResultReno1
    #cat resultReno2 | grep sec | head -15 | tr - " " | awk '{print $4, $8}' > newResultReno2
    #cat resultCubic1 | grep sec | head -15 | tr - " " | awk '{print $4, $8}' > newResultCubic1
    #cat resultCubic2 | grep sec | head -15 | tr - " " | awk '{print $4, $8}' > newResultCubic2
    #gnuplot
    #plot "newResultReno1" title "tcp_flow" with linespoints 
    #set xlabel "time (sec)" 
    #set ylabel "througput (Gbps)" 
    #replot

    #rp_disable(r1)
    #rp_disable(net['r2'])
    # net[ 'r1'].cmd('ip route add to 10.10.6.0/24 via 10.10.5.2')
    # net[ 'r1'].cmd('ip route add to 10.10.7.0/24 via 10.10.5.2')
    # net[ 'r1'].cmd('ip route add to 10.10.8.0/24 via 10.10.5.2')
    # net[ 'r1'].cmd('ip route add to 10.10.9.0/24 via 10.10.5.2')
   


    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    perfTest()
