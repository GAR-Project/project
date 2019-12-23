# GAR-Project 2019-2020

   This workgroup is a project created by 4 students of the University of Alcalá for the subject of Network Management and Administration of the fourth year.

<br>

## Guides (spanish):
*  Network Scenario - Mininet Guide: [Link](https://hackmd.io/@davidcawork/r1fZC-nRS) 

<br>

## TODO

 * ~~Setting up a network scenario with Mininet.~~ :heavy_check_mark:
 * ~~Choice of tools to recreate the DDoS attack.~~  (**ping y hping3**) :heavy_check_mark:
 * Run telegraf on the 'test' machine, and on the 'control' machine InfluxDB and Grafana.
 * Using the InfluxDB interface ([Python API](https://github.com/influxdata/influxdb-python)) create a script that implements an AI algorithm that classifies whether we are under a DDoS attack or in a normal traffic situation.
        
 * See how we can import the output of the script that decides if a DDos is running into the Grafana dashboard, to reflect it generate alarms and so on.
 
 * **[Optional]** Knowing if we're under attack, How we can mitigate it? we should get into the logic of the Ryu app ([`simple_switch_13.py`](https://github.com/osrg/ryu/blob/master/ryu/app/simple_switch_13.py))
 
<br>

---

## Installation methods  🔧

For the installation of the scenario, a Vagrant image has been created to which all the shellscripts necessary for the installation/configuration of the scenario are supplied. It has been chosen to have all the same specifications, this way, in case of finding errors we will be able to trace their cause in an easier way. If you do not want to use the Vagrant installation method you can follow the native installation method.

### Vagrant
We make a clone of the repository:
```bash
git clone https://github.com/GAR-Project/project
cd project
```
We power up the virtual machine:
```bash
vagrant up
```

And we have to connect to both machines:
```bash
vagrant ssh test
vagrant ssh controller
```

We should already have all the machines configured with all the necessary tools to raise our network scenario with Mininet on the VM **test**, and Ryu on the VM **controller**.

#### Troubleshooting - ssh connection
If you have problems connecting via ssh to the machine, check that the keys in the path `.vagrant/machines/test/virtualbox/` are owned by the user, and have read-only permissions for the owner of the key. 

``` bash
cd .vagrant/machines/test/virtualbox/
chmod 400 private_key

# We can also do this (u,g,o -> user, group, others)
chmod u=r,go= private_key
```
Instead of using the vagrant manager to make the ssh connection, we can ultimately make the connection ourselves by entering the path to the private key. For example:

```bash
ssh -i .vagrant/machines/test/virtualbox/private_key vagrant@10.0.123.2
```

---

### Native
As it is a native installation it is understood that the user has the virtual machine already pre-configured. Ideally there should be two VMs to separate the controller from the VM where the network topology will be emulated. Try to use a Ubuntu 16.04 distribution.

We make a clone of the repository:
```bash
git clone https://github.com/GAR-Project/project
cd project
```

We launched the provisioning shellscript, each on its own machine:
```bash
# To install Mininet and Mininet dep
sudo ./util/provisioning.sh

# To install Ryu
sudo ./util/ryu.sh

```

---

## Our scenario
Our network scenario is described in the script [`src/scenario_basic.py`](https://github.com/GAR-Project/project/blob/master/src/scenario_basic.py). Mininet makes use of a Python API to give users the ability to automate processes easily, or to develop certain modules at their convenience. For this and many other reasons, Mininet is a highly flexible and powerful tool for network emulation (widely used by the scientific community). 

* For more information about the API, see its [manual](http://mininet.org/api/annotated.html).


![Escenario](https://i.imgur.com/kH7kAqB.png)

For this scenario, the controller has been separated into a virtual machine and the network core into another virtual machine. In Mininet we identify the controller, **Ryu**, by the IP of the virtual machine within the VirtualBox private network and its listening port. This separation into two different machines is due to the following:


* Facilitate teamwork, since the **logic with AI** will go directly into the controller's MV. In this way the integration of teamwork will be easier, making the Mininet core + data collection (**telegraf**) independent from the DDoS attack detection logic, visualization (**Grafana** + **InfluxDB**). 

* Facilitate the storage of data to InfluxDB from telegraf, as due to the internal workings of Mininet there may be conflicts in the communication of this data. The basic operation of Mininet at a low level will be detailed below.

* By separating in two machines with clearly differentiated functionalities it is possible to make debug in a simpler way since we will be able to identify in a clear way which of these modules (Mininet Core, Controller) give problems.

### How to run our scenario
To run our scenario we must be connected with uan end to the virtual machine `test` and the virutal machine `controller`. First of all we're going to power up the controller, to do this from the controller machine we run the following, it's an application that does a basic forwarding, which is what we need:


```
ryu-manager ryu.app.simple_switch_13
```
![ryu_up](https://i.imgur.com/EGyKHLT.png)

Once the controller is up we are going to execute the core of the network, to do this from the 'test' machine we are going to launch the above mentioned scritp:


```
sudo python3 scenario_basic.py
```
![mininet_up](https://i.imgur.com/DSPsPDL.png)

You can also see that from our test machine we have opened the so-called **CLI of Mininet**. It is a command line interface from which you can do many actions. The most useful one will be detailed below.

### Is working properly?
We'd have our operational scenario by now. We can check our network connectivity by pinging the hosts, for example:

``` bash
mininet> h1 ping h3


# We can also ping each other with the pingall command
mininet> pingall
```

![ping_basic](https://i.imgur.com/NhglFK5.png)
<br>
As you can see in the image above, there is full connectivity in our scenario. As a curiosity, **Why does it take so long for the first ping message?** , it is normal, we have to take into account that the first ping message before being transmitted must be done the following actions:

* ARP resolution between sender and receiver of the ping, in order to obtain the MACs and form the packets. 

* In addition, the ICMP (ping-request) package will be redirected to the driver to decide what to do with the package, as it does not have a specified **Flow** with a rule set on the switches through which the ping-request and ping-reply will pass. This way the controller will, when it receives the packet, instantiate a set of rules on the switches so that the ICMP packet is routed from one host to another.

![ryu_packet_in](https://i.imgur.com/lSGDeTN.png)

<br>

As you can see, in the stdout of the controller, it indicates the commands it has been instantiating according to the packages it has processed. In the end, for the first package you will have to assume a delay due to ARP resolution and rule resolution with the controller. But the rest of the packets will already have the destination MAC and the rules instantiated in the intermediate switches, so their delay time will be minimal.

---

## Mininet CLI 
We've already set up our scenario and verified that it's working properly. We will now detail the most important commands of Mininet's CLI.

### Command: EOF + quit + exit
These three commands are used for the same thing, to exit the Mininet CLI and finish the emulation. The source code of these three commands do not differ much, **EOF** and **quit** end up using exit at the end, so we could say that they are a bit repetitive.

```python
def do_exit( self, _line ):
    "Exit"
    assert self # satisfy pylint and allow override
    return 'exited by user command'

def do_quit( self, line ):
    "Exit"
    return self.do_exit( line )

def do_EOF( self, line ):
    "Exit"
    output( '\n' )
    return self.do_exit( line )
```

### Command: dpctl
The **dpctl** command is a management utility command that allows some control over the OpenFlow switch (ovs-ofctl on the OpenvSwitch). With this command it is possible to add flows to the flow table, check the features and status of the switches or clean the table among many other things. For example, previously we made a ping between **h1** to **h3**, if we consult the flow tables we will be able to check how the rules have been instantiated for this type of flows:

![dpctl](https://i.imgur.com/1N3yQm8.png)

You can see how a rule has been urged to go and return in those switches through which our ping fluctuates.

This command is very extensive, and it may not be completely necessary for what we are going to do in this practice, but it is undoubtedly one of the most important commands to understand the internal workings of SDN switches. For more information, consult its documentation:

*    [OpenvSwitch](http://www.openvswitch.org/support/dist-docs/ovs-ofctl.8.txt)


### Command: dump + net
These commands will give us information about the emulated topology. The command **net** will indicate the names of the entities in the topology to be emulated and their interfaces. The **dump** command will also indicate the type of entity, IP address, port when applicable, interface and the process identifier (pid) of the entity.

![dump](https://i.imgur.com/ysCDTE5.png)

### Command: xterm + gterm

These two commands will allow us to open terminals in the indicated node. The command **xterm** will allow us to open a simple terminal, and the command **gterm** will allow us to open a gnome-terminal. We can open several terminals at once by indicating all the nodes we want to open a terminal in. Later, when we enter the inner workings of Mininet, some details will be explained about where this bash process is running. You might think that this process is isolated from the machine on which you are running Mininet, but this is not entirely the case.

```bash
# xterm/gterm [node1] [node2]

xterm h1 h6
```

![xterm](https://i.imgur.com/YkSj6QB.png)


### Command: nodes + ports + intfs

These commands will list information related to the nodes in the topology. The command **intfs** will list all information related to the nodes' interfaces. The command **nodes** will list all nodes in the topology. Finally, the command **ports**, used to list the ports and interfaces of the switches in the topology.

![intfs](https://i.imgur.com/9qNNYy1.png)

### Command: The rest of the commands :smirk: 

Look at it in with the **help** command, or else ask me directly, I didn't want this part to grow too much. With the above commands it is understood that all the needs of the project will be covered.

<br>

---

<br>

## Mininet Internals

As previously mentioned, Mininet is a tool used to emulate SDN networks. I stress that it is important to know the difference between **emulation** and **simulation**. With the simulation we will use a software that calculates events of an expected behavior, and with the emulation, we recreate the whole scenario in a specific hardware and see how it behaves. To see it in a simpler way, we could say that playing an airplane videogame would be a simulation. But for example, practicing in a 1:1 scale flight deck with real controls could be considered an emulation.

![emulación](https://i.imgur.com/Pwr6MHb.jpg)


Once we understand the difference, let's move on to the next step. **Mininet Emulates?** Yes, Mininet emulates the behavior of a network by reserving resources on your machine for each element of the network to be emulated. You might think that each network element is a virtual machine or a virtualized container...

But it is not, that solution although it has many advantages since it completely assimilates the node, it has a very important contra which is the resources that would be used in the host machine. So, for example, we would not be able to emulate a fairly large network on a single machine due to lack of resources. The solution that the Mininet developers chose was to **virtualize exclusively** what was necessary to perform the **network emulation**.

How did they do it? By using the Network Namespaces.

<br>

### Network Namespaces

A **network namespace** consists of a logical network stack replica that by default has the Linux kernel, paths, ARP tables, Iptables and network interfaces.

Linux starts with a default Network namespace, with its routing table, with its ARP table, with its Iptables and network interfaces. But it is also possible to create more non-default network namespaces, create new devices in those namespaces, or move an existing device from one namespace to another. This is a rather complex virtualization concept provided by the linux kernel, I will not go further :fearful:.

In this way, each network element has its own network namespace, i.e. each element has its own network stack and interfaces. So at the networking level, as you would say, they can be seen as independent elements. 

Although they all share process namepace, IPCs namespace, the same file system...

![example](https://i.imgur.com/4ihZdsP.png)


For example, I put in the host machine I create a process with PID **20483**, with the command **sleep**. If the network elements were isolated, they would not be able to see the processes on the host machine, however the reality with Mininet is different. 

This is something to assume when working with Mininet, low-cost emulation :sweat_smile: . Although I repeat, to emulate a network is more than enough. What we should see is how to integrate our data collection system (telegraph) in the different elements of the network without incompatibilities. 

That's why it was decided to take the controller out of this machine where Mininet was going to run, to avoid problems with by-passes by IPCs from telegraph to the InfluxDB database. So it would only remain to see how to install telegraf and configure it correctly so that it works as agreed.



---
## Troubleshooting

* If we use a terminal, without **X server** for example, to reroute the graphical stdout of the virtual machine out, the Miniedit tool will not run. It uses tkinter, it needs the environment variable `$DISPLAY` properly configured. 


* If there are problems when launching the scenario try to clean the previous environment. Normally if we go out with the mininet CLI quit command it should be deleted correctly, otherwise we can always clean it up ourselves:
```
sudo mn -c
```
![clean](https://i.imgur.com/zRrxiP5.png)


### Authors ✒️

* **David Carrascal** - [Link github](https://github.com/davidcawork)
* **Adrián Guerrero** - [Link github](https://github.com/adrihamel)
* **Pablo Collado** - [Link github](https://github.com/pcolladosoto)
* **Artem Strilets** - [Link github](https://github.com/ArtemSSOO)


### Wiki 📖

_Fuentes del proyecto_
