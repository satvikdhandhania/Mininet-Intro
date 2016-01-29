#!/usr/bin/python
#Author Satvik Dhandhania (sdhandha) Date: 01/28/2016

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink

class SingleSwitchTopo(Topo):
    def build(self):
        #Creating 6 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        
        #Add 6 hosts to the network
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')
        
        #Adding links between switches 
        self.addLink(s1,s2, bw=10, delay='1ms', loss=3)
        self.addLink(s4,s2, bw=20, delay='4ms', loss=1)
        self.addLink(s1,s3, bw=15, delay='2ms', loss=2)
        self.addLink(s3,s5, bw=20, delay='4ms', loss=1)
        self.addLink(s5,s6, bw=40, delay='10ms', loss=2)

        #Adding links between switches and hosts
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)
        self.addLink(h5, s4)
        self.addLink(h6, s5)
        self.addLink(h7, s6)
        self.addLink(h8, s6)

def simpleTest():
    #Create and test a the network
    topo = SingleSwitchTopo()
    net = Mininet(topo, link=TCLink)
    net.start()
    print 'Dumping host connections'
    dumpNodeConnections(net.hosts)
    #Pinging to and fro between each pair of hosts in the network
    print '\n\n\n\nTesting network connectivity - PING\n\n'
    
    for i in range(1,9):
        for j in range(1,9):
            if(i!=j):
                print '\n\nTesting between h%s & h%s'%(i,j)
                h1,h2, = net.get('h%s'%(i),'h%s'%(j))
                print h1.cmd('ping -c10 %s' % h2.IP())


    #Testing TCP bandwidth of each pair of hosts making a server client pair
    print '\n\n\n\nMeasuring TCP Bandwidth between each pair of hosts\n\n'
    for i in range(1,9):
        h1=net.get('h%s'%i)
        result=h1.cmd('iperf3 -s &')
        print result
        print 'Done running iperf on server h%s, starting client now'%(i)
        for j in range(1,9):
            if(i!=j):
                print '\n\nTesting between h%s & h%s'%(i,j)
                h2=net.get('h%s'%j)
                print 'Now testing bandwidth'
                result1=h2.cmd('iperf3 -c %s'%(h1.IP()))
                print result1 
        print 'Shutting down the iperf server'
        h1.cmd('kill -9 $pid')


    #Testing UDP bandwidth of each pair of hosts making a server client pair
    print '\n\n\n\nMeasuring UDP Bandwidth between each pair of hosts'
    print 'Packet loss between each pair in percentage in brackets\n\n'
    for i in range(1,9):
        h1=net.get('h%s'%i)
        print 'Starting server h%s'%(i)
        result=h1.cmd('iperf -u -s &')
        print result
        print 'Done running iperf on server h%s, starting client now'
        for j in range(1,9):
            if(i!=j):
                print '\n\nTesting between h%s & h%s'%(i,j)
                h2=net.get('h%s'%j)
                print 'Now testing bandwidth'
                result1=h2.cmd('iperf -c %s -u  -b 15000000'%(h1.IP()))
                print result1 
        print 'Shutting down the iperf server'
        h1.cmd('kill -9 $pid')

    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
