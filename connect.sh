#!/bin/bash

echo 'Starting script'
echo '...Make sure the module is ready'
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode='online'

echo '...Configuring network interface for the raw-ip protocol'
sudo ip link set wwan0 down
echo 'Y' | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set wwan0 up

echo '...connect the mobile network'
sudo qmicli -p -d /dev/cdc-wdm0 --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network="apn='nxtgenphone',ip-type=4" --client-no-release-cid

echo '...Configuring the IP address and the default route with udhcpc'
ADDRESS = 'sudo udhcpc -q -f -i wwan0'
echo $ADDRESS

