#!/bin/sh

#Grafana
sudo apt-get -f install

sudo apt-get install -y apt-transport-https
sudo apt-get install -y software-properties-common wget
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -

sudo apt update
sudo apt upgrade
sudo apt install grafana

wget https://dl.grafana.com/oss/release/grafana_6.5.2_amd64.deb
sudo apt install -y adduser libfontconfig1
sudo dpkg -i grafana_6.5.2_amd64.deb

sudo systemctl daemon-reload
sudo systemctl start grafana-server
sudo systemctl status grafana-server
sudo systemctl enable grafana-server.service


#InfluxDB
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/lsb-release
echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt-get update && sudo apt-get install influxdb
sudo systemctl unmask influxdb.service
sudo systemctl start influxdb

#etc.