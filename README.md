# GAR-Project 2019-2020

   This workgroup is a project created by 4 students of the University of Alcalá for the subject of Network Management and Administration of the fourth year.

<br>

## Guides (spanish):
*  Network Scenario - Mininet Guide: [Link](https://hackmd.io/@davidcawork/r1fZC-nRS) 

<br>

## TODO

 * ~~Setting up a network scenario with Mininet.~~ :heavy_check_mark:
 * ~~Choice of tools to recreate the DDoS attack.~~ -> **ping y hping3** :heavy_check_mark:
 * Run telegraf on the 'test' machine. Run InfluxDB and Grafana on the 'control' machine.
 * Using InfluxDB's interface ([Python API](https://github.com/influxdata/influxdb-python)) create a script that implements an AI algorithm that deterrmines whether we are under a DDoS attack or in a normal traffic situation through classification.
        
 * See how we can import the output of the script that decides if a DDos is running into the Grafana dashboard, to reflect it generate alarms and so on.
 
   **IDEA**: Manually add a measurement in *telegraf* that tells us whether or not we are under attack in a binary fashion and monitor it from *Grafana* in the usual way. I gues we can easily insert data into *InfluxDB* from *Python* :thinking_face:
 
 * **[Optional]** Knowing if we're under attack, How we can mitigate it? We should get into the logic of the Ryu app ([`simple_switch_13.py`](https://github.com/osrg/ryu/blob/master/ryu/app/simple_switch_13.py)) and try to take action from there.
 
<br>

---

## Notes
Throughout the document we will always be talking about 2 virtual machines (VMs) on which we implement the scenario we are discussing. In order to keep it simple we hace called one VM **controller** and the other one **mininet**. Even though the names may seem kind of random at the moment we promise they're not. Just keep this in mind as you continue reading.

<br>

---

## Installation methods  🔧

We have created a **Vagrantfile** through which we provide each machine with the necessary scripts to install and configure the scenario. Working in a virtualized environment we make sure we all have the exact same configuration so that tracing and fixing erros becomes much easier. If you do not want to use Vagrant as a provider you can follow the native installation method we present below.

### Vagrant
First of all, clone the repository from GitHub :octocat: and navigate into the new directory with:
```bash
git clone https://github.com/GAR-Project/project
cd project
```
We power up the virtual machine through **Vagrant**:
```bash
vagrant up
```

And we have to connect to both machines. **Vagrant** provides a wrapper for the *SSH* utility that makes it a breeze to get into each virtual machine. The syntax is just `vagrant ssh <machine_name>` where the `<machine_name>` is given in the **Vagrantfile** (see the [appendix](#appendix)):
```bash
vagrant ssh test
vagrant ssh controller
```

We should already have all the machines configured with all the necessary tools to bring our network up with Mininet on the **test** VM, and Ryu on the **controller** VM .

#### Troubleshooting problems regarding SSH
If you have problems connecting via SSH to the machine, check that the keys in the path `.vagrant/machines/test/virtualbox/` are owned by the user, and have read-only permissions for the owner of the key. 

``` bash
cd .vagrant/machines/test/virtualbox/
chmod 400 private_key

# We could also use this instead of "chmod 400" (u,g,o -> user, group, others)
# chmod u=r,go= private_key
```
Instead of using vagrant's manager to make the SSH connection, we can opt for manually doing it ourselves by passing the path to the private key to SSH. For example:

```bash
ssh -i .vagrant/machines/test/virtualbox/private_key vagrant@10.0.123.2
```

---

### Native
This method assumes you already have any VMs up and running with the correct configuration and dependencies installed. Ideally you should have 2 VMs. We will be running **Ryu** (the *SDN* controller) in one of them and we will have **mininet**'s emulated network with running in the other one. Try to use Ubuntu 16.04 (a.k.a **Xenial**) as the VM's distribution to avoid any mistakes we may have not encountered.

First of all clone the repository, just like how the Kaminoans do it and then navigate into it:
```bash
git clone https://github.com/GAR-Project/project
cd project
```

Manually launch the provisioning script in each machine:
```bash
# To install Mininet and Mininet's dependencies. Run it on the "mininet" VM
sudo ./util/provisioning.sh

# To install Ryu. Run it on the "controller" VM
sudo ./util/ryu.sh
```

---

## Our scenario
Our network scenario is described in the following script: [`src/scenario_basic.py`](https://github.com/GAR-Project/project/blob/master/src/scenario_basic.py). Mininet makes use of a Python API to give users the ability to automate processes easily, or to develop certain modules at their convenience. For this and many other reasons, Mininet is a highly flexible and powerful tool for network emulation which is widely used by the scientific community. 

* For more information about the API, see its [manual](http://mininet.org/api/annotated.html).


<!--![Escenario](https://i.imgur.com/kH7kAqB.png)-->
<!-- Using HTML let's us center images! It's kind of dirty though... -->
<p align="center">
    <img src="https://i.imgur.com/kH7kAqB.png">
</p>

The image above presents us with the *logic* scenario we will be working with. As with many other areas in networking this logic picture doesn't correspond with the real implementation we are using. We have seen throughout the installation procedure how we are always talking about 2 VMs. If you read carefully you'll see that one VM's "names" are **controller** and **mininet**. So it should come as no surprise that the controller and the network itself are living in different machines!

The first question that may arise is how on Earth can we logically join these 2 together. When working with virtualized enviroments we will generate a virtual LAN where each VM is able to communicate with one another. Once we stop thinking about programs and abstract the idea of "*process*" we find that we can easily identify the **controller** which is just a **ryu** app, which is nothing more than a **python3** app with the **controller**'s VM **IP** address and the port number where the **ryu** is listening. We shouldn't forget that **any** process running within **any** host in the entire **Internet** can be identified with the host's **IP** address and the processes **port** number. Isn't it amazing?

Ok, the above sounds great but... Why should we let the controller live in a machine when we could have everything in a single machine and call it a day? We have our reasons:

* Facilitate teamwork, since the **AI's logic** will go directly into the controller's VM. This let's us increase both working group's independence. One may work on the mininet core and the data collection with **telegraf** whilst the other can look into the DDoS attack detection logic and visualization using **Grafana** and **InfluxDB**. 

* Facilitate the storage of data into **InfluxDB** from **telegraf**, as due to the internal workings of Mininet there may be conflicts in the communication of said data. Mininet's basic operation at a low level is be detailed below.

* Having two different environments relying on distinct tools and implementing different functionalities let's us identify and debug problems way faster. We can know what piece of software is causing problems right away!

### Running the scenario
Running the scenario requires having logged into both VMs manually or using vagrant's SSH wrapper. First of all we're going to power up the controller, to do so we run the following from the `controller` VM. It's an application that does a basic forwarding, which is just what we need:

```
ryu-manager ryu.app.simple_switch_13
```

<!--![ryu_up](https://i.imgur.com/EGyKHLT.png)-->

<p align="center">
    <img src="https://i.imgur.com/EGyKHLT.png">
</p>

Once the controller is up we are going to execute the network itself, to do this from the `test` machine we are going to launch the aforementioned mentioned script:

```
sudo python3 scenario_basic.py
```

<!--![mininet_up](https://i.imgur.com/DSPsPDL.png)-->

<p align="center">
    <img src="https://i.imgur.com/DSPsPDL.png">
</p>

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

## Appendix <a name="appendix"></a>


### Authors ✒️

* **David Carrascal** - [Link github](https://github.com/davidcawork)
* **Adrián Guerrero** - [Link github](https://github.com/adrihamel)
* **Pablo Collado** - [Link github](https://github.com/pcolladosoto)
* **Artem Strilets** - [Link github](https://github.com/ArtemSSOO)


### Wiki 📖

*Fuentes del proyecto*
