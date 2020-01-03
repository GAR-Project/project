# -*- mode: ruby -*-
# vi: set ft=ruby :
# encoding: UTF-8

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/xenial64"
  # Added graphics forwarding thanks to the X11 server so that
  # I could open a XTERM terminal in my system. This concerns
  # native linux users mostly!
  config.ssh.forward_agent = true
  config.ssh.forward_x11 = true
  config.vm.provider "virtualbox" do |v|
  v.customize ["modifyvm", :id, "--memory", 1024]
  end

  config.vm.define "test" do |test|
    test.vm.hostname = 'test'
    test.vm.network :private_network,ip:"10.0.123.2"
    test.vm.provision "shell", :path => "./util/install_mininet.sh"
    # My Vagrant version complains with the other file provisioning... I had to tweak it for my system
    # Uncomment the latter to use a more robust provisioning. As we only use one config file it's ok for us!
    test.vm.provision "file", source: "./conf/telegraf_mn_host.conf", destination: "/home/vagrant/conf/telegraf_mn_host.conf"
    test.vm.provision "file", source: "./conf/telegraf_test_2_controller.conf", destination: "/home/vagrant/conf/telegraf.conf"
    test.vm.provision "shell", :path => "./util/install_telegraf.sh"
    test.vm.provision "file", source: "./src/scenario_basic.py", destination: "/home/vagrant/scenario_basic.py"
    test.vm.provision "file", source: "./src/ddos.py", destination: "/home/vagrant/ddos.py"
    test.vm.provision "file", source: "./src/normal.py", destination: "/home/vagrant/normal.py"
  end
  
  config.vm.define "controller" do |controller|
    controller.vm.hostname = 'controller'
    controller.vm.network :private_network,ip:"10.0.123.3"
    controller.vm.provision "shell", :path => "./util/install_ryu.sh"
    controller.vm.provision "shell", :path => "./util/install_grafana_influxdb.sh"
    controller.vm.provision "file", source: "./src/traffic_classifier.py", destination: "/home/vagrant/traffic_clasifier.py"
    controller.vm.provision "file", source: "./training_datasets/ICMP_data_class_0.csv", destination: "/home/vagrant/training_datasets/ICMP_data_class_0.csv"
    controller.vm.provision "file", source: "./training_datasets/ICMP_data_class_1.csv", destination: "/home/vagrant/training_datasets/ICMP_data_class_1.csv"
  end
end
