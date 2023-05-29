#!/bin/bash

# Specify the line number in the destination file where you want to write the contents
line_number=10

# Specify the source file (the file whose contents you want to write)
source_file="/home/ubuntu/cluster-keys.pub"

# Specify the destination file (the file where you want to write the contents)
destination_file="/home/ubuntu/Github-analytic-system-using-pulsar/consumer-cfg.txt"

# Read the contents of the source file
contents=$(cat "$source_file")


mkdir -p /home/ubuntu/cluster-keys
ssh-keygen -f /home/ubuntu/cluster-keys/cluster-key -N “”-t rsa
sed -i "${line_number}i\\
$contents
" "$destination_file"
