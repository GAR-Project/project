#!/usr/bin/python
# -*- coding: utf-8 -*-

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController, Ryu
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def scenario_basic():
    net = Mininet(  topo = None,
                    build = False,
                    host = CPULimitedHost,
                    link = TCLink,
                    ipBase = '10.0.0.0/8')

    info('*** Add Controller (Ryu) ***\n')
    c0 = net.addController( name = 'c0',
                            controller = RemoteController,
                            ip = '10.0.123.3',
                            protocol = 'tcp',
                            port = 6633)

    info('*** Add three switchs ***\n')
    s1 = net.addSwitch('s1', cls = OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls = OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls = OVSKernelSwitch)

    info('*** Add Host ***\n')
    h1 = net.addHost('h1', cls = Host, ip = '10.0.0.1', defaultRoute = None)
    h2 = net.addHost('h2', cls = Host, ip = '10.0.0.2', defaultRoute = None)
    h3 = net.addHost('h3', cls = Host, ip = '10.0.0.3', defaultRoute = None)
    h4 = net.addHost('h4', cls = Host, ip = '10.0.0.4', defaultRoute = None)
    h5 = net.addHost('h5', cls = Host, ip = '10.0.0.5', defaultRoute = None)
    h6 = net.addHost('h6', cls = Host, ip = '10.0.0.6', defaultRoute = None)

    info('*** Add links ***\n')
    net.addLink(s1, h1, bw = 10)
    net.addLink(s1, h2, bw = 10)
    net.addLink(s1, s2, bw = 5, max_queue_size = 500)
    net.addLink(s3, s1, bw = 5, max_queue_size = 500)
    net.addLink(s2, h3, bw = 10)
    net.addLink(s2, h4, bw = 10)
    net.addLink(s3, h5, bw = 10)
    net.addLink(s3, h6, bw = 10)

    info('\n*** Build it ***\n')
    net.build()

    info('*** Start the controller ***\n')
    for controller in net.controllers:
        controller.start()

    info('*** Set controllers ***\n')
    # Notice how [c0] returns a list of controller objects whose only element
    # is c0. The start() method will traverse the input parameter with a for
    # loop so we need to pass a list as an argument...
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s1').start([c0])

    info('\n*** Start Telegraf ***\n')
    # Notice that s1, s2 and s3 are in the same Network Namespace.
    # net.get('s1').cmd('telegraf --config conf/telegraf.conf &')
    # We need to run telegraf in the hosts because the have ICMP visibility
    # The switches can only see up to layer 2...
    net.get('h4').cmd('telegraf --config conf/telegraf_mn_host.conf &')

    info('*** RUN Mininet\'s CLI ***\n')
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    scenario_basic()

