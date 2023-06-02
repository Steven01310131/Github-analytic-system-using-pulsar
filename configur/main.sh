#!/bin/bash
sudo apt update
sudo apt -y upgrade
sudo apt install default-jre
sudo apt install python3-pip -y
wget https://archive.apache.org/dist/pulsar/pulsar-2.7.0/apache-pulsar-2.7.0bin.tar.gz
tar xvfz apache-pulsar-2.7.0-bin.tar.gz
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
cd apache-pulsar-2.7.0
docker run -d -it -p 6650:6650 -p 8080:8080 \
--mount source=pulsardata,target=/pulsar/data \
--mount source=pulsarconf,target=/pulsar/conf \
apachepulsar/pulsar:2.7.0 bin/pulsar standalone

git clone https://github.com/Steven01310131/Github-analytic-system-using-pulsar
source /home/ubuntu/Github-analytic-system-using-pulsar/configur/UPPMAX_2023_1-1-openrc.sh
/home/ubuntu/Github-analytic-system-using-pulsar/configur/nova.sh
/home/ubuntu/Github-analytic-system-using-pulsar/configur/ansible.sh
/home/ubuntu/Github-analytic-system-using-pulsar/configur/keygen.sh
python3 /home/ubuntu/Github-analytic-system-using-pulsar/start_instances.py | grep "^192" > ip_consumers.txt
/home/ubuntu/Github-analytic-system-using-pulsar/configur/cpyip.sh
python3 /home/ubuntu/Github-analytic-system-using-pulsar/producer.py
ansible-playbook /home/ubuntu/Github-analytic-system-using-pulsar/custom_ansible/consumers.yml