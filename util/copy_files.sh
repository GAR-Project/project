#!/bin/sh

#Move
sudo mv datasources.yaml /etc/grafana/provisioning/datasources/datasources.yaml
sudo mkdir /var/lib/grafana/dashboards
sudo cp project.json /var/lib/grafana/dashboards/
sudo cp main.yaml /etc/grafana/provisioning/dashboards/main.yaml