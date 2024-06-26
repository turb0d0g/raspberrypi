#!/bin/bash
# Read voltage from i2c if Wittypi is 
# mounted run with `bash witty_voltage.sh`

readonly I2C_MC_ADDRESS=0x08 readonly 
I2C_VOLTAGE_IN_I=1 readonly 
I2C_VOLTAGE_IN_D=2 

i2c_read() {
  local retry=0 
  if [ $# -gt 3 ]; then 
    retry=$4
  fi 
  local result=$(/usr/sbin/i2cget -y $1 $2 $3) 
  if [[ "$result" =~ ^0x[0-9a-fA-F]{2}$ ]]; 
then
    echo $result; 
  else 
    retry=$(( $retry + 1 )) 
    if [ $retry -ne 4 ]; then
      sleep 1 
      i2c_read $1 $2 $3 $retry 
    else 
      echo "Error reading I2C value" >&2 
      return 1
    fi 
  fi
}

calc() { 
  awk "BEGIN { print $*}";
}

i=$(i2c_read 0x01 $I2C_MC_ADDRESS 
$I2C_VOLTAGE_IN_I) 
d=$(i2c_read 0x01 
$I2C_MC_ADDRESS $I2C_VOLTAGE_IN_D) 
if [[ -z 
$i ]] || [[ -z $d ]]; then
  echo "Failed to read voltage values." 
  exit 1
fi 

calc $(($i))+$(($d))/100
exit 0
