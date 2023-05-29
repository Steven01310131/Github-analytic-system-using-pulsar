#!/bin/bash

prepend_file="/home/ubuntu/Github-analytic-system-using-pulsar/ip_consumers.txt"
destination_file="/home/ubuntu/Github-analytic-system-using-pulsar/custom_ansible/inventory.txt"

# Prepend lines from the prepend file to corresponding lines in the destination file
paste -d"\0" <(cat "$prepend_file") "$destination_file" > temp_file
mv temp_file "$destination_file"
