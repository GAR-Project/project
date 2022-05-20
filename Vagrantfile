VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # The machines will be running Ubuntu 20.04 Focal Fossa
  config.vm.box = "ubuntu/focal64"

  # These settings enable X11 forwarding so that native
    # Linux users can just run a graphic application
    # on the VMs and have that displayed by their local
    # X11 server. This concerns the `xterm` command on
    # mininet, for instance.
  config.ssh.forward_agent = true
  config.ssh.forward_x11 = true

  # We'll allocate 1 GiB of memory to each VM.
  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory", 1024]
  end

  # Let's configure the machine running MiniNet machine.
  config.vm.define "test" do |test|
    # The machines hostname is, well, test xD
    test.vm.hostname = 'test'

    # It'll be assiged IPv4 address 10.0.123.2 on VirtualBox's NATted network.
    test.vm.network :private_network,ip:"10.0.123.2"

     # We'll copy all the necessary files to their apropriate destinations within the VM upon creation too!
     test.vm.provision "file", source: "./conf/telegraf_mn_host.conf", destination: "/home/vagrant/conf/telegraf_mn_host.conf"
     test.vm.provision "file", source: "./conf/telegraf_test_2_controller.conf", destination: "/home/vagrant/conf/telegraf.conf"
     test.vm.provision "file", source: "./src/scenario_basic.py", destination: "/home/vagrant/scenario_basic.py"
     test.vm.provision "file", source: "./src/ddos.py", destination: "/home/vagrant/ddos.py"
     test.vm.provision "file", source: "./src/normal.py", destination: "/home/vagrant/normal.py"

    # We'll run the following scripts to install sboth mininet and Telegraf when creating the VM.
    test.vm.provision "shell", :path => "./util/install_mininet.sh"
    test.vm.provision "shell", :path => "./util/install_telegraf.sh"
  end

  # Time to configure the machine running Ryu.
  config.vm.define "controller" do |controller|
    # The machine's name is, not surprisingly, controller.
    controller.vm.hostname = 'controller'

    # It'll be assigned IPv4 address 10.0.123.3 within VirtualBox's NATted network.
    controller.vm.network :private_network,ip:"10.0.123.3"

    # We'll copy files to their appropriate destination within the VM upon creation.
    controller.vm.provision "file", source: "./conf/datasources.yaml", destination: "/home/vagrant/datasources.yaml"
    controller.vm.provision "file", source: "./conf/main.yaml", destination: "/home/vagrant/main.yaml"
    controller.vm.provision "file", source: "./conf/project_dashboard.json", destination: "/home/vagrant/project.json"
    controller.vm.provision "file", source: "./src/traffic_classifier.py", destination: "/home/vagrant/traffic_clasifier.py"
    controller.vm.provision "file", source: "./training_datasets/ICMP_data_class_0.csv", destination: "/home/vagrant/training_datasets/ICMP_data_class_0.csv"
    controller.vm.provision "file", source: "./training_datasets/ICMP_data_class_1.csv", destination: "/home/vagrant/training_datasets/ICMP_data_class_1.csv"

    # With files prepared we'll run the following to install Ryu, InfluxDB, Grafana and finally automatically configure Grafana.
    controller.vm.provision "shell", :path => "./util/install_ryu.sh"
    controller.vm.provision "shell", :path => "./util/install_grafana_influxdb.sh"
    controller.vm.provision "shell", :path => "./util/copy_files.sh"
  end
end
