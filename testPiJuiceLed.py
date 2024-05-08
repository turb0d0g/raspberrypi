#!/usr/bin/python3
import os 
import logging 
from pijuice import PiJuice 

pj = PiJuice(1,0x14)

# Show custom script is run by blinking the 
# user LED red 10x
pj.status.SetLedBlink('D1', 2, [200,200,200], 50, [200, 200, 200], 50)
#pj.status.
