#!/usr/bin/python

"""
linuxrouter.py: Example network with Linux IP router

This example converts a Node into a router using IP forwarding
already built into Linux.

The example topology creates a router and three IP subnets:

    - 192.168.1.0/24 (r0-eth1, IP: 192.168.1.1)
    - 172.16.0.0/12 (r0-eth2, IP: 172.16.0.1)
    - 10.0.0.0/8 (r0-eth3, IP: 10.0.0.1)

Each subnet consists of a single host connected to
a single switch:

    r0-eth1 - s1-eth1 - h1-eth0 (IP: 192.168.1.100)
    r0-eth2 - s2-eth1 - h2-eth0 (IP: 172.16.0.100)
    r0-eth3 - s3-eth1 - h3-eth0 (IP: 10.0.0.100)

The example relies on default routing entries that are
automatically created for each router interface, as well
as 'defaultRoute' parameters for the host interfaces.

Additional routes may be added to the router or hosts by
executing 'ip route' or 'route' commands on the router or hosts.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    def build( self, **_opts ):

        r0_eth1 = '192.168.1.1/24'  # IP address for r0-eth1
        r1_eth1 = '192.168.1.2/24'

        r0 = self.addNode( 'r0', cls=LinuxRouter, ip=r0_eth1 )
        r1 = self.addNode( 'r1', cls=LinuxRouter, ip=r1_eth1 )
        defaultIP = {
            "h1":"10.0.1.100",
            "h2":"10.0.2.100",
            "h3":"10.0.3.100",
            "h4":"10.0.4.100",
            "h5":"10.20.1.100",
            "h6":"10.20.2.100",
            "h7":"10.20.3.100",
            "h8":"10.20.4.100"
        }
        defaultVia = {
            "h1":"via 10.0.1.1",
            "h2":"via 10.0.2.1",
            "h3":"via 10.0.3.1",
            "h4":"via 10.0.4.1",
            "h5":"via 10.20.1.1",
            "h6":"via 10.20.2.1",
            "h7":"via 10.20.3.1",
            "h8":"via 10.20.4.1"
        }

        

        s1, s2, s3 = [ self.addSwitch( s ) for s in 's1', 's2', 's3' ]

        self.addLink(r0, r1, intfName1='r0-eth1', params1={'ip':r0_eth1}, intfName2='r1-eth1', params2={'ip':r1_eth1})

        h1 = self.addHost('h1', ip='10.0.1.100', defaultRoute='via 10.0.1.1')
        self.addLink(h1, r0, intfName2='r0-eth2', params2={'ip':'10.0.1.1/24'})
        # h2 = self.addHost('h2', ip=defaultIP['h2'], defaultRoute=defaultVia['h2'])
        # h3 = self.addHost('h3', ip=defaultIP['h3'], defaultRoute=defaultVia['h3'])
        # h4 = self.addHost('h4', ip=defaultIP['h4'], defaultRoute=defaultVia['h4'])
        # h5 = self.addHost('h5', ip=defaultIP['h5'], defaultRoute=defaultVia['h5'])
        # h6 = self.addHost('h6', ip=defaultIP['h6'], defaultRoute=defaultVia['h6'])
        # h7 = self.addHost('h7', ip=defaultIP['h7'], defaultRoute=defaultVia['h7'])
        # h8 = self.addHost('h8', ip=defaultIP['h8'], defaultRoute=defaultVia['h8'])

        # self.addLink(h2, r0, intfName2='r0-eth3', params2={'ip':'10.0.2.1/24'})
        # self.addLink(h3, r0, intfName2='r0-eth4', params2={'ip':'10.0.3.1/24'})
        # self.addLink(h4, r0, intfName2='r0-eth5', params2={'ip':'10.0.4.1/24'})

        # self.addLink(h5, r1, intfName2='r1-eth2', params2={'ip':'10.20.1.1/24'})
        # self.addLink(h6, r1, intfName2='r1-eth3', params2={'ip':'10.20.2.1/24'})
        # self.addLink(h7, r1, intfName2='r1-eth4', params2={'ip':'10.20.3.1/24'})
        # self.addLink(h8, r1, intfName2='r1-eth5', params2={'ip':'10.20.4.1/24'})


        # self.addLink( s1, r0, intfName2='r0-eth6', params2={ 'ip' : '10.128.0.1/24' } )  # for clarity
        # self.addLink( s2, r0, intfName2='r0-eth7', params2={ 'ip' : '172.16.0.1/12' } )
        # self.addLink( s3, r0, intfName2='r0-eth8', params2={ 'ip' : '10.64.0.1/24' } )

        # h1 = self.addHost( 'h1', ip='192.168.1.100/24',
        #                    defaultRoute='via 192.168.1.1' )
        # h2 = self.addHost( 'h2', ip='172.16.0.100/12',
        #                    defaultRoute='via 172.16.0.1' )
        # h3 = self.addHost( 'h3', ip='10.0.0.100/8',
        #                    defaultRoute='via 10.0.0.1' )

        # for h, s in [ (h1, s1), (h2, s2), (h3, s3) ]:
        #     self.addLink( h, s )


def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo )  # controller is used by s1-s3
    net.start()
    info( '*** Routing Table on Router:\n' )
    print net[ 'r0' ].cmd( 'route' )
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
