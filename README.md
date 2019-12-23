# GAR-Project 2019-2020

   This workgroup is a project created by 4 students of the University of Alcalá for the subject of Network Management and Administration of the fourth year

## Guides (spanish):
*  Network Scenario - Mininet Guide: [Link](https://hackmd.io/@davidcawork/r1fZC-nRS) 

## TODO

 * ~~Plantear un escenario de red con Mininet.~~ :white_check_mark:
 * ~~Elección de herramientas para recrear el ataque DDoS.~~  (**ping y hping3**) :white_check_mark:
 * Poner a funcionar telegraf en la máquina `test`, y en la máquina `controller` InfluxDB y grafana.
 * Haciendo uso de la interfaz de InfluxDB ([API Python](https://github.com/influxdata/influxdb-python)) crear un script que implemente algoritmo de AI que clasifique si estamos bajo un ataque DDoS o en una situación de tráfico normal.
        
 * Ver como podemos importar el output del script que decide si hay un DDos en marcha hacia el dashboard de Grafana, para así reflejarlo generar alarmas y demás.
 
 * **[Opcional]** Sabiendo si estamos bajo ataque, como podemos mitigarlo, habría que meterse en la lógica de la app de Ryu ([`simple_switch_13.py`](https://github.com/osrg/ryu/blob/master/ryu/app/simple_switch_13.py))
 
 
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



### Run tests ⚙️

_Ejecución de pruebas del proyecto_

### Authors ✒️

* **David Carrascal** - [Link github](https://github.com/davidcawork)
* **Adrián Guerrero** - [Link github](https://github.com/adrihamel)
* **Pablo Collado** - [Link github](https://github.com/pcolladosoto)
* **Artem Strilets** - [Link github](https://github.com/ArtemSSOO)



### Wiki 📖

_Fuentes del proyecto_
