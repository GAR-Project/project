## TODO

 * ~~Setting up a network scenario with Mininet.~~ :heavy_check_mark:

 * ~~Choice of tools to recreate the DDoS attack.~~ --> We've chosen **ping and hping3** :heavy_check_mark:

 * ~~Run telegraf on the 'test' machine. Run InfluxDB and Grafana on the 'control' machine.~~ :heavy_check_mark:

 * ~~Using InfluxDB's interface ([Python API](https://github.com/influxdata/influxdb-python)) create a script that implements an AI algorithm that deterrmines whether we are under a DDoS attack or in a normal traffic situation through classification.~~ :heavy_check_mark:

 * ~~See how we can import the output of the script that decides if a DDos is running into the Grafana dashboard, to reflect it generate alarms and so on.~~ :heavy_check_mark:

 * ~~**IDEA**: Manually add a measurement in *telegraf* that tells us whether or not we are under attack in a binary fashion and monitor it from *Grafana* in the usual way. I gues we can easily insert data into *InfluxDB* from *Python* :panda_face:~~ :heavy_check_mark:

 * ~~See how we can export data from InfluxDB and how we can manipulate it.~~ :heavy_check_mark:

 * ~~Choose an AI algorithmig for traffic classification~~ --> **SVM** (**S**upport **V**ector **M**achines) :heavy_check_mark:

 * **[Optional]** Knowing if we're under attack, How we can mitigate it? We should get into the logic of the Ryu app ([`simple_switch_13.py`](https://github.com/osrg/ryu/blob/master/ryu/app/simple_switch_13.py)) and try to take action from there.

 * ~~Complete the appendix section.~~ :heavy_check_mark:

 * Get all the documentation in LaTeX format

 * Get the presentation ready

 
