# GAR-Project 2019-2020

   This workgroup is a project created by 4 students of the University of Alcalá for the subject of Network Management and Administration of the fourth year.

<br>

## Guides (spanish):
*  Network Scenario - Mininet Guide: [Link](https://hackmd.io/@davidcawork/r1fZC-nRS) 
*  DDoS using hping3 tool Guide: [Link](https://hackmd.io/@davidcawork/HJ_D7jA0r)
*  Mininet Internals (II) Guide: [Link](https://hackmd.io/@davidcawork/SyrwHoNJL)

<br>

## TODO

 * ~~Setting up a network scenario with Mininet.~~ :heavy_check_mark:
 * ~~Choice of tools to recreate the DDoS attack.~~ --> We've chosen **ping and hping3** :heavy_check_mark:
 * ~~Run telegraf on the 'test' machine. Run InfluxDB and Grafana on the 'control' machine.~~ :heavy_check_mark:
 * Using InfluxDB's interface ([Python API](https://github.com/influxdata/influxdb-python)) create a script that implements an AI algorithm that deterrmines whether we are under a DDoS attack or in a normal traffic situation through classification.
        
 * ~~See how we can import the output of the script that decides if a DDos is running into the Grafana dashboard, to reflect it generate alarms and so on.~~ :heavy_check_mark:
 
   ~~**IDEA**: Manually add a measurement in *telegraf* that tells us whether or not we are under attack in a binary fashion and monitor it from *Grafana* in the usual way. I gues we can easily insert data into *InfluxDB* from *Python* :panda_face:~~ :heavy_check_mark:
 
 * ~~See how we can export data from InfluxDB and how we can manipulate it.~~ :heavy_check_mark:
 
 * ~~Choose an AI algorithmig for traffic classification~~ --> **SVM** (**S**upport **V**ector **M**achines) :heavy_check_mark:
 
 * **[Optional]** Knowing if we're under attack, How we can mitigate it? We should get into the logic of the Ryu app ([`simple_switch_13.py`](https://github.com/osrg/ryu/blob/master/ryu/app/simple_switch_13.py)) and try to take action from there.
 * Complete the appendix section
 * Get all the documentation in LaTeX format
 * Get the presentation ready

 
<br>

---

## Notes
Throughout the document we will always be talking about 2 virtual machines (VMs) on which we implement the scenario we are discussing. In order to keep it simple we hace called one VM **controller** and the other one **mininet**. Even though the names may seem kind of random at the moment we promise they're not. Just keep this in mind as you continue reading.

<br>

---

## Installation methods :wrench:

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

First of all clone the repository, just like how the Kaminoans :alien: do it and then navigate into it:
```bash
git clone https://github.com/GAR-Project/project
cd project
```

Manually launch the provisioning scripts in each machine:
```bash
# To install Mininet, Mininet's dependencies and telegraf. Run it on the "mininet" VM
sudo ./util/install_mininet.sh
sudo ./util/install_telegraf.sh

# To install Ryu and Monitoring system (Grafana + InfluxDB). Run it on the "controller" VM
sudo ./util/install_ryu.sh
sudo ./util/install_grafana_influxdb.sh
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

You might prefer to run the controller in the background as it doesn't provide really meaningful information. In order to do so we'll run:

```
ryu-manager ryu.app.simple_switch_13 > /dev/null 2>&1 &
```

Let's break this big boy down:

* `> /dev/null` redirects the `stdout` file descriptor to a file located in `/dev/null`. This is a "special" file in linux systems that behaves pretty much like a black hole. Anything you write to it just "disappears" :open_mouth:. This way we get rid of all the bloat caused by the network startup.

* `2>&1` will make the `stderr` file descriptor point where the `stdout` file descriptor is currently pointing (`/dev/null`). Terminal emulators usually have both `stdout` and `stderr`"going into" the terminal itself so we need to redirect these two to be sure we won't see any output.

* `&` makes the process run in the background so that you'll be given a new prompt as soon as you run the command.

If you want to move the controller app back into the foreground so that you can kill it with `CTRL + C` you can run `fg` which will bring the last process sent to the background back to the foreground.


<!-- ![ryu_up](https://i.imgur.com/EGyKHLT.png) -->

<p align="center">
    <img src="https://i.imgur.com/EGyKHLT.png">
</p>

Once the controller is up we are going to execute the network itself, to do so launch the aforementioned script from the `test` machine:

```
sudo python3 scenario_basic.py
```

<!-- ![mininet_up](https://i.imgur.com/DSPsPDL.png) -->

<p align="center">
    <img src="https://i.imgur.com/DSPsPDL.png">
</p>

Notice how we have opened **Mininet CLI** from the `test` machine. We can perform many actions from this command line interface. The most useful ones are detailed below.

### Is working properly?
We should have our scenario working as intended by now. We can check our network connectivity by pinging the hosts, for example:

``` bash
mininet> h1 ping h3

# We can also ping each other with the pingall command
mininet> pingall
```

<!-- ![ping_basic](https://i.imgur.com/NhglFK5.png) -->

<p align="center">
    <img src="https://i.imgur.com/NhglFK5.png">
</p>

As you can see in the image above, there is full connectivity in our scenario. You may have noticed how the first **ping** takes way longer than the other to get back to use. That is, its **RTT** (**R**ound **T**rip **T**ime) is abnormally high. This is due to the empty **ARP** tables we currently have *AND* to the fact that we don't yet have a flow defined to handle **ICMP** traffic:

* An **ARP** resolution between sender and receiver of the ping takes place so that the sender learns the next hop's **MAC** address.

* In addition, the **ICMP** message (ping-request) will be redirected to the driver (a.k.a controller) to decide what to do with the packet as the switches don't yet have a **flow** to handle this traffic type. This way the controller will, when it receives the packet, instantiate a set of rules on the switches so that the **ICMP** messages are routed from one host to the other.

<!-- ![ryu_packet_in](https://i.imgur.com/lSGDeTN.png) -->

<p align="center">
    <img src="https://i.imgur.com/lSGDeTN.png">
</p>

<br>

As you can see, the controller's **stdout** (please see the [appendix](#appendix) to learn more about file descriptors) indicates the commands it has been instantiating according to the packets it has processed. In the end, for the first packet we will have to tolerate a delay due to **ARP** resolution and **flow** lookup and instantiation within the controller. The good thing is the rest of the packets will already have the destination **MAC** and the rules will already instantiated in the intermediate switches, so the new delay will be minimal.

### Attack time! :boom:

<div style="text-align: justify">

We have already talked about how to set up our scenario but we haven't got into breaking things (i.e the fun stuff :smiling_imp:). Our goal is to simulate a **DoS** (**D**enial **o**f **Service**) attack. Note that we usually refer to this kind of threats as **DDoS** attacks where the first **D** stands for **D**istributed. This second "name" implies that we have multiple machines trying to flood our own. We are going to launch the needed amounts of traffic from a single host so we would be making a mistake if we were talking about a distributed attack. All in all this is just a minor nitpick, the concept behind both attacks is exactly the same.

We need to flood the network with traffic, great but... How should we do it? We already introduced the tool we are going to be using: **hping3**. This program was born as a TCP/IP packet assembler and analyzer capable of generating ICMP traffic. Its biggest asset is being able to generate these ICMP messages as fast as the machine running it can: just what we need :japanese_goblin:.

The main objective is being able to classify the traffic in the network as a normal or an abnormal situation with the help of AI algorithms. For these algorithms to be effective we need some training samples so that they can "learn" how to regard and classify said traffic. That's why we need a second tool capable of generating "normal" ICMP traffic so that we have something to compare against. Good ol' **ping** is our pal here.

</div>

#### Time to limit the links

<div style="text-align: justify">

We should no mention our scenario again. We had a **Ryu** controller, three **OVS** switches and several hosts "hanging" from these switches. The question is: **what's the capacity of the network links?**

<!-- ![escenario](https://i.imgur.com/aeteCr9.png) -->

According to Mininet's [wiki](https://github.com/mininet/mininet/wiki/Introduction-to-Mininet) that capacity is not limited in the sense that the network will be able to handle as much traffic as the hardware emulating it can. This implies that the more powerful the machine, the larger the link capacity will be. This poses a problem to our experiment as we want it to be reproducible in any host. That's why we have decided to limit each link's bandwidth during the network setup.

This behaviour is a consequence of Mininet's implementation. We'll discuss it [here](#mininet_internals) later down the road but the key aspect is that we cannot neglect Mininet's implementation when making design choices!

<br>

</div>

##### How to limit them

<div style="text-align: center">

<br>

In order to limit the available **BW** (**B**and **W**idth) we'll use Mininet's API. This API is just a wrapper for a **TC** (**T**raffic **C**ontroller) who is in charge of modifying the kernel's **planner** (i.e *Network Scheduler*). The code where we leverage the above is:

```python
net = Mininet(topo = None,
              build = False,
              host = CPULimitedHost,
              link = TCLink,
              ipBase = '10.0.0.0/8')
```

Note how we need to limit each host's capacity by means of the CPU which is what we do through the `host` parameter in Mininet's contructor. We'll also need links with a `TCLink` type. We can achieve this thanks to the `link` parameter. This will let us impose the limits to the network capacity ourselves instead of depending on the host's machines capabilities.

<br>

After fiddling with the overall constructor we also need to take care when defining the network links. We can find the following lines over at **src/scenario_basic.py**:

```python
net.addLink(s1, h1, bw = 10)
net.addLink(s1, h2, bw = 10)
net.addLink(s1, s2, bw = 5, max_queue_size = 500)
net.addLink(s3, s1, bw = 5, max_queue_size = 500)
net.addLink(s2, h3, bw = 10)
net.addLink(s2, h4, bw = 10)
net.addLink(s3, h5, bw = 10)
net.addLink(s3, h6, bw = 10)
```

We are fixing a **BW** for the links with the `bw` parameter. We have also chosen to assign a finite buffer size to the middle switches in an effor to get as close to reality as we possibly can. If the `max_queue_size` parameter hadn't been defined we would be working with "infinite" buffers at each switch's exit ports. Having these finite buffers will in fact introduce a damping effect in our tests as onece you fill them up you can't push any more data through: the output queues are absolutely full... In a real-life scenario we would suffer huge packet losses at the switches and that could be used as a symptom as well but we haven't taken it into accoun for the sake of simplicity.

We fixed the queue lengths so that they were coherent with standard values. We decided to use a **500 packet** size because *Cisco*'s (:satisfied:) queue lengths range from 64 packets to about 1000 as found [here](https://www.cisco.com/c/en/us/support/docs/routers/7200-series-routers/110850-queue-limit-output-drops-ios.html). We felt like 500 was an appropriate value in the middle ground. With all these restrictions our scenario would look like this:

<!-- ![limits](https://i.imgur.com/pzCf5GJ.png) -->

<p align="center">
    <img src="https://i.imgur.com/pzCf5GJ.png">
</p>

By inspecting the network dimensions we can see how we have a clear bottleneck... This "flaw" has been introduced on purpose as we want to clearly differentiate regurlar traffic from the one we experience when under attack.

</div>

#### Getting used to hping3

<div style="text-align: justify">

This versatile tool can be configured so that it can explore a given network, perform traceroutes, send pings or carry out out flood attacks on different network layers. All in all, it lets us craft our own packets and send them to different destinations at some given rates. You can even forge the source **IP** address to go full stealth mode :ghost:. We'll just send regular pings: **ICMP --> Echo request (Type = 8, Code = 0)** whilst increasing the rate at which we send them. This will in turn make the network core collapse making our attack successful.

Check out this [site](https://tools.kali.org/information-gathering/hping3) for more info on this awesome tool.

</div>

#### Installing things... again! :weary:

<div style="text-align: justify">

The tool will be already present on the test machine as it was included in the **Vagrantfile** as part of the VM's provisioning script. In case you want to manually install it you can just run the command below as **hping3** is usually within the default software sources:

```
sudo apt install hping3
```

</div>

#### Usage

<div style="text-align: jsutify">

As we have previously discussed this is quite a complete tool so we will only use one of the many functionalities to keep things simple. The command we'll be using is:

```
hping3 -V -1 -d 1400 --faster <Dest_IP>
```

We are going to break down each of the options:

* `-V`: Show verbose output (i.e show more information)
* `-1`: Generate ICMP packets. They'll be ping requests by default
* `-d 1400`: Add a bogus payload. This is not strictly needed but it'll help us use up the link's BW faster. We have chosen a 1400 B payload so as not to suffer fragmentation at the network layer.
* `--faster`:

<br>

We would like to point out that `hping3` could have been invoked with the `--flood` option instead of `--faster`. When using `--flood` the machine will generate as many packets as it possibly can. This would be great in a world of rainbows but... The virtual network was quickly overwhelmed by the ICMP messages and packets began to be discarded everywhere. Event though this is technically a **DoS** attack gone right too it obscures the phenomena we are faster so we decided to use `--faster` as the rate it provides suffices for our needs.

</div>

---

#### Demo time! :tada:

<div style="text-align: justify">

The attack we are going to carry out comprises hosts **1**, **2** and **4**. We'll launch `hping3` from **Host1** targeting **Host4** and we'll try to ping **Host4** from **Host2**. We will in fact see how this "regular" ping doesn't get through as a consequence of a successful **DoS** attack. The image below depicts the situation:

<!-- ![ataque](https://i.imgur.com/awt7e5v.png) -->

<p align="center">
    <img src="https://i.imgur.com/awt7e5v.png">
</p>

Let's begin by setting up the scenario like we usually do:

```bash
sudo python3 scenario_basic.py
```

Time to open terminals to both ICMP sources. We'll also fire up `Wireshark` on **Host4** to have a closer look at what's going on. Note the ampersand (`&`) at the end of the second command. It'll detach the `wireshark` process from the terminal so that we can continue running commands as we normally would. To do this we need to run:

```bash
mininet> xterm h1 h2
mininet> h4 wireshark &
```

<br>

Time to launch `hping3` from **Host1** with the parameters we discussed:

<p align="center">
    <img src="https://i.imgur.com/Uei0gb5.png">
</p>

<br>

If we now try to ping **Host4** from **Host2** we'll fail horribly:

<p align="center">
    <img src="https://i.imgur.com/yjfSJoD.png">
</p>

<br>

If we halt the **DoS** attack we will see the regular traffic resume its normal operation after a short period of time:

<p align="center">
    <img src="https://i.imgur.com/5fkmrEu.png">
</p>

<br>

We then see how the **DoS** attack against **Host4** has been successful. In order to facilitate issuing the needed commands we have prepared a couple of `python` scripts containing all the needed information so that we only need to run them and be happy. You can find them at:

* Attack: [`src/ddos.py`](https://github.com/GAR-Project/project/blob/master/src/ddos.py)
* Regular traffic: [`src/normal.py`](https://github.com/GAR-Project/project/blob/master/src/normal.py)

With all this ready to rock we now need to focus on detecting these attacks and seeing how to possibly mitigate them.

</div>

#### Wanted a video?

<div style="text-align: justify">

You can find a video showing the process we described step by step (click the image to follow the link :smirk_cat:). If you stumble upon any questions don't hesitate to contact us! :grin:

<p align="center">
    <a href="https://www.youtube.com/watch?v=ofZPmV6_y_M">
        <img src="https://img.youtube.com/vi/ofZPmV6_y_M/0.jpg">
    </a>
</p>

</div>

---

## Mininet CLI 
We've already set up our scenario and verified that it's working properly. We will now detail the most important commands we can issue from of **Mininet's CLI**.

### Command: EOF + quit + exit
These three commands are used for the same thing, to exit the **Mininet CLI** and finish the emulation. The source code of these three commands does not differ much, **EOF** and **quit** end up using the `do_exit` function at the end, so we could say that they are a bit repetitive. They offer several ways to kill the emulation so that people with different backgrounds feel "at `~`". The source code taking care of exiting is:

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
The **dpctl** command is a management utility that allows some control over the OpenFlow switch (ovs-ofctl on the OpenvSwitch). This tool lets us add flows to the flow table, check the features and status of the switches or clean the table among many other things. For example, recall how we previously made a ping between **h1** and **h3**. If we consult the flow tables we will be able to check how the rules for handling **ICMP** flows have been instantiated:

<!-- ![dpctl](https://i.imgur.com/1N3yQm8.png) -->

<p align="center">
    <img src="https://i.imgur.com/1N3yQm8.png">
</p>

Note how in the first and third switches we have 3 flow instead of the default one that let's us communicate with the controller. On top of that, take a closer look at the third switch and notice how the input and output ports for the first flow are 3 and 1 respectively. The second rule has the exact opposite distribution: the input port is 1 and the output is port 3. This setup let's us establish a communication link through this switch between any machines hooked to port's 1 and 3. These are the rules the controller has automagically set for us!

This command is quite complex and powerful, and it may not be completely necessary for what we are going to do in this practice. It is nevertheless undoubtedly one of the most important commands to understand the internal workings of **SDN** switches. For more information, we encourage you to take a look at the documentation over at [OpenvSwitch](http://www.openvswitch.org/support/dist-docs/ovs-ofctl.8.txt).

### Command: dump + net
These commands will give us information about the emulated topology. The **net** command will indicate the names of the entities in the emulated topology as well as their interfaces. The **dump** command will also indicate the type of entity, its **IP** address, port when applicable, interface and the entitie's process identifier (**PID**).

<!-- ![dump](https://i.imgur.com/ysCDTE5.png) -->

<p align="center">
    <img src="https://i.imgur.com/ysCDTE5.png">
</p>

### Command: xterm + gterm
These two commands will allow us to open terminal emulators in the node identified by the accompanying argument. The command **xterm** will allow us to open a simple **XTERM** (the default terminal emulator for the **X** windows system) terminal emulator, and **gterm** launches a prettier but more resource hungry **Gnome terminal**. We can open several terminals at once by indicating all the nodes we want to open a terminal in. Later, when we discuss the inner workings of **Mininet**, we'll talk a bit more about where the **bash** process attached to the terminal emulator is running. You might think that this process is totally isolated from the machine on which you are running **Mininet**, but this is not entirely the case...

```bash
# xterm/gterm [node1] [node2]
xterm h1 h6
```

<!-- ![xterm](https://i.imgur.com/YkSj6QB.png) -->

<p align="center">
    <img src="https://i.imgur.com/YkSj6QB.png">
</p>


### Command: nodes + ports + intfs
These commands will list information related to the nodes in the topology. The **intfs** command will list all information related to the nodes' interfaces. The  **nodes** command will show every node in the topology. Finally, the **ports** command is used to list the ports and interfaces of the switches in the topology.

<!-- ![intfs](https://i.imgur.com/9qNNYy1.png) -->

<p align="center">
    <img src="https://i.imgur.com/9qNNYy1.png">
</p>

### Command: The rest of the commands :smirk:
Someone once told me **manpages** were my friends. This doesn't apply here directly but you get the idea. If you don't know what a command does try running it without arguments and you will be presented with a help section hopefully. If your machine blows up... It wasn't our fault! (It really should't though :ok_woman:). You can also issue `help <command_name>` from the **mininet CLI** to gather more intel. You can also contact us directly. We didn't want this section to grow too large and we believe the above commands are more than enough for our purposes.

<br>

---

<br>

## Mininet Internals <a name="mininet_internals"></a>

We have been covering **Mininet** fow a while now but... What is exactly **Mininet**? It is a tool used for emulating **SDN** (**S**oftware **D**efined **N**etworks). We can write software programs describing the network topology we want and then run them to create a virtual network just like the one we described. Cool right?

Now, notice how we used the term **emulation** instead of **simulation**. Even though many people regard these terms as equivalent they are **NOT** the same. When we talk about **simulation** we are referring to software that computes the outcome of an event given an expected behaviour. On the other hand, **emulation** recreates the scenario under study in its entirety on specific hardware to then study its behaviour.

An example to differentiate the two could be to think about a plane cockpit. If we were to play a videogame like **Flight Simulator** we would be simulating (no surprise) the flight but if we were to practice using a 1:1 scale with real controls we would then be talking about emulation.

<!-- ![emulación](https://i.imgur.com/Pwr6MHb.jpg) -->

<p align="center">
    <img src="https://i.imgur.com/Pwr6MHb.jpg">
</p>


With this little detail out of the way we could ask ourselves. Does **mininet** emulate or simulate a network?. It is a network **emulator**, here's why. Mininet resrves system resources for each node in the **emulated** network. You might think these nodes are "just" VMs or virtualized containers but... they're not. That solution would have many advantages but it wouldn't scale to be able to **emulate** large networks or huge ammounts of traffic as it would exhaust the host system's resources... The Mininet developers then chose to **exclusively virtualize** what was necessary to carry out the desired **network emulation**.

How did they do it? By using the **Network Namespaces**.

<br>

### Network Namespaces

A **network namespace** consists of a logical network stack replica that by default is composed of the **Linux kernel**, paths, **ARP** tables, **Iptables** and network interfaces.

Linux starts with a default **Network namespace** which is the one everyday users need for example. This namespace includes a routing table, an ARP table, the Iptables and any network interfaces it might need. The key here is that it is also possible to create more non-default network namespaces. We can then create new devices in those namespaces, or move an existing devices from one namespace to another. This is a rather complex virtualization concept provided by the Linux kernel and we will not delve any further. It is quite interesting if you ask us though... :fearful:

In this way, each network element has its own network namespace, i.e. each element has its own network stack and interfaces. So at the networking level, one could say, they are independent elements. The key is that every node shares the same process namespace, IPCs namespace, filesystem... We are virtualizing up to the network layer only. This is the true power of the network stack approach to things. As Vegeta would put it: "Tha network namespace's power is over 9000!". **TODO**: Insert Meme here.

<!-- ![example](https://i.imgur.com/4ihZdsP.png) -->

<p align="center">
    <img src="https://i.imgur.com/4ihZdsP.png">
</p>

In the above image we can see how we created a process in the host machine with the `sleep` command whose **PID** is `20483`. If the network elements were really isolated we wouldn't be able to see this process from other machines but the reality is different with mininet as we discussed.

This is something to assume when working with Mininet's low-cost emulation :sweat_smile:. This approach would be lacking in other scenarios but it is more than enough to emulate a network. This fact casts some doubts on how to integrate our data collection system with **telegraf** in the different network elements without any incompatibilities...

That's why we decided to take the controller "out of" the machine where Mininet was going to run so as to avoid problems with by-passes by IPCs from telegraf to the InfluxDB database. The only thing left for us to do is to figure out how to correctly install and configure telegraf so that everything works as intended.

---
## Troubleshooting

<!-- * If we use a terminal, without **X server** for example, to reroute the graphical stdout of the virtual machine out, the Miniedit tool will not run. It uses tkinter, it needs the environment variable `$DISPLAY` properly configured. -->

* If we are to use a terminal emulator without an **X server** installed or properly configured the **miniedit** tool will not run. This tool presents us with a GUI we can use to define our network and then it'll generate a script that brings it up for us. If we are to reroute the **stdout** of a VM we will need to set the `$DISPLAY` variable accordingly as **miniedit** used **tkinter** and it needs it to run correctly.


* If there are problems when launching the scenario try to clean up the previous environment. If we exit the mininet CLI by issuing the `quit` everything should be deleted correctly, otherwise we can always clean it up ourselves by running:
```bash
sudo mn -c
```
<!-- ![clean](https://i.imgur.com/zRrxiP5.png) -->

<p align="center">
    <img src="https://i.imgur.com/zRrxiP5.png">
</p>

## Appendix <a name="appendix"></a>
* TODO: Talk about the Vagrantfile
* TODO: Talk about file descriptors (stdout)


### Authors :black_nib:

* **David Carrascal** -> [Link github](https://github.com/davidcawork)
* **Adrián Guerrero** -> [Link github](https://github.com/adrihamel)
* **Pablo Collado** -> [Link github](https://github.com/pcolladosoto)
* **Artem Strilets** -> [Link github](https://github.com/ArtemSSOO)


### Wiki :book:

*Fuentes del proyecto*
