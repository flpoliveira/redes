from mininet.net import Mininet

from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch

from mininet.cli import CLI

from mininet.log import setLogLevel

from mininet.link import Link, TCLink



def topology():

        net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )



        # Add hosts and switches

        h1 = net.addHost( 'h1', ip="10.0.1.10/24", mac="00:00:00:00:00:01" )
        h2 = net.addHost( 'h2', ip="10.0.1.20/24", mac="00:00:00:00:00:03" )
        h3 = net.addHost( 'h3', ip="10.0.1.30/24", mac="00:00:00:00:00:05" )
        h4 = net.addHost( 'h4', ip="10.0.1.40/24", mac="00:00:00:00:00:07" )

        server1 = net.addHost( 'server1', ip="10.0.2.10/24", mac="00:00:00:00:00:02" )
        server2 = net.addHost( 'server2', ip="10.0.2.20/24", mac="00:00:00:00:00:04" )
        server3 = net.addHost( 'server3', ip="10.0.2.30/24", mac="00:00:00:00:00:06" )
        server4 = net.addHost( 'server4', ip="10.0.2.40/24", mac="00:00:00:00:00:08" )


        r1 = net.addHost( 'r1')

        r2 = net.addHost( 'r2')

        s1 = net.addSwitch( 's1')

        s2 = net.addSwitch( 's2')

        c0 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )



        net.addLink( r1, s1 )

        net.addLink( r2, s2 )

        net.addLink( r1, r2 )

        net.addLink( h1, s1 )
        net.addLink( h2, s1 )
        net.addLink( h3, s1 )
        net.addLink( h4, s1 )

        net.addLink( server1, s2 )
        net.addLink( server2, s2 )
        net.addLink( server3, s2 )
        net.addLink( server4, s2 )

        net.build()

        c0.start()

        s1.start( [c0] )

        s2.start( [c0] )

        r1.cmd("ifconfig r1-eth0 0")

        r1.cmd("ifconfig r1-eth1 0")

        r1.cmd("ifconfig r1-eth0 hw ether 00:00:00:00:01:01")

        r1.cmd("ifconfig r1-eth1 hw ether 00:00:00:00:01:03")

        r1.cmd("ip addr add 10.0.1.1/24 brd + dev r1-eth0")

        r1.cmd("ip addr add 10.0.3.1/24 brd + dev r1-eth1")

        r1.cmd('sysctl net.ipv4.ip_forward=1')

        r2.cmd("ifconfig r2-eth0 0")

        r2.cmd("ifconfig r2-eth1 0")

        r2.cmd("ifconfig r2-eth0 hw ether 00:00:00:00:01:02")
        r2.cmd("ifconfig r2-eth1 hw ether 00:00:00:00:01:04")

        r2.cmd("ip addr add 10.0.2.1/24 brd + dev r2-eth0")
        r2.cmd("ip addr add 10.0.3.2/24 brd + dev r2-eth1")

        r2.cmd('sysctl net.ipv4.ip_forward=1')


        h1.cmd("ip route add default via 10.0.1.1")
        h2.cmd("ip route add default via 10.0.1.1")
        h3.cmd("ip route add default via 10.0.1.1")
        h4.cmd("ip route add default via 10.0.1.1")

        server1.cmd("ip route add default via 10.0.2.1")
        server2.cmd("ip route add default via 10.0.2.1")
        server3.cmd("ip route add default via 10.0.2.1")
        server4.cmd("ip route add default via 10.0.2.1")

        r1.cmd("ip route add default via 10.0.3.2")
        r2.cmd("ip route add default via 10.0.3.1")

        s1.cmd("ovs-ofctl add-flow s1 priority=1,arp,actions=flood")
        s1.cmd("ovs-ofctl add-flow s1 priority=65535,ip,dl_dst=00:00:00:00:01:01,actions=output:1")
        s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.1.10,actions=output:2")
        s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.1.20,actions=output:3")
        s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.1.30,actions=output:4")
        s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.1.40,actions=output:5")

        s2.cmd("ovs-ofctl add-flow s2 priority=1,arp,actions=flood")
        s2.cmd("ovs-ofctl add-flow s2 priority=65535,ip,dl_dst=00:00:00:00:01:02,actions=output:1")
        s2.cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.0.2.10,actions=output:2")
        s2.cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.0.2.20,actions=output:3")
        s2.cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.0.2.30,actions=output:4")
        s2.cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.0.2.40,actions=output:5")

        print "*** Running CLI"

        CLI( net )



        print "*** Stopping network"

        net.stop()



if __name__ == '__main__':

    setLogLevel( 'info' )

    topology()
