# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, random, re
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session


flavor = "ssc.medium"
private_net = "UPPMAX 2023/1-1 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "Ubuntu 22.04 - 2023.01.07"

identifier = random.randint(1000,9999)

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print ("user authorization completed.")

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/consumer-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata_consumer = open(cfg_file_path)
else:
    sys.exit("consumer-cfg.txt is not in current working directory")

# cfg_file_path =  os.getcwd()+'/dev-cloud-cfg.txt'
# if os.path.isfile(cfg_file_path):
#     userdata_dev = open(cfg_file_path)
# else:
#     sys.exit("dev-cloud-cfg.txt is not in current working directory")    

secgroups = ['default']

print ("Creating instances ... ")
instance_consumer = nova.servers.create(name="consumer_group16_"+str(identifier), image=image, flavor=flavor, key_name='DataEngi',userdata=userdata_consumer, nics=nics,security_groups=secgroups)
#instance_dev = nova.servers.create(name="dev_server_"+str(identifier), image=image, flavor=flavor, key_name='<KEY-NAME>',userdata=userdata_dev, nics=nics,security_groups=secgroups)
inst_status_consumer = instance_consumer.status
#inst_status_dev = instance_dev.status

print ("waiting for 10 seconds.. ")
time.sleep(10)

while inst_status_consumer == 'BUILD':
    print ("Instance: "+instance_consumer.name+" is in "+inst_status_consumer+" state, sleeping for 5 seconds more...")
    #print ("Instance: "+instance_dev.name+" is in "+inst_status_dev+" state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance_consumer = nova.servers.get(instance_consumer.id)
    inst_status_consumer = instance_consumer.status
    #instance_dev = nova.servers.get(instance_dev.id)
    #inst_status_dev = instance_dev.status

ip_address_consumer = None
for network in instance_consumer.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_consumer = network
        break
if ip_address_consumer is None:
    raise RuntimeError('No IP address assigned!')

# ip_address_dev = None
# for network in instance_dev.networks[private_net]:
#     if re.match('\d+\.\d+\.\d+\.\d+', network):
#         ip_address_dev = network
#         break
# if ip_address_dev is None:
#     raise RuntimeError('No IP address assigned!')

print ("Instance: "+ instance_consumer.name +" is in " + inst_status_consumer + " state" + " ip address: "+ ip_address_consumer)
#print ("Instance: "+ instance_dev.name +" is in " + inst_status_dev + " state" + " ip address: "+ ip_address_dev)