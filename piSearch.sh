#!/bin/bash
SAVEIFS=$IFS
IFS=$'\n'
echo "Searching network for Raspberry Pis"

pis=( $(nmap -sP `ip -o -f inet addr show | grep \`ip route get 1 | awk '{print $NF;exit}'\` | awk '{print $4}'` | awk '/^Nmap/{ip=gensub(/[^0-9\.]/,"","g", $NF);host=$(NF-1)}/B8:27:EB/{printf "%s\t%s\t%s\n", ip, $3, host}') )
echo
echo "Found ${#pis[@]} pis"
echo
printf '%s\n' "${pis[@]}"
IFS=$SAVEIFS