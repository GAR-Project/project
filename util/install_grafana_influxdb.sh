#!/bin/sh

#Grafana
sudo apt-get -fy install && apt-get install -y libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_6.5.2_amd64.deb
sudo dpkg -i grafana_6.5.2_amd64.deb
sudo systemctl start grafana-server
rm grafana_6.5.2_amd64.deb

#InfluxDB
wget https://dl.influxdata.com/influxdb/releases/influxdb_1.7.9_amd64.deb
sudo dpkg -i influxdb_1.7.9_amd64.deb
sudo apt-get update && apt-get install -yq python3-influxdb
sudo systemctl start influxd
rm influxdb_1.7.9_amd64.deb
