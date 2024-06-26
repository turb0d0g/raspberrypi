#!/bin/bash

GPIOA=17
GPIOB=27
test -e /sys/class/gpio/gpio$GPIOA || (echo $GPIOA > /sys/class/gpio/export && echo in > /sys/class/gpio/gpio$GPIOA/direction)
test -e /sys/class/gpio/gpio$GPIOB || (echo $GPIOB > /sys/class/gpio/export && echo in > /sys/class/gpio/gpio$GPIOB/direction)
valA=$(cat /sys/class/gpio/gpio$GPIOA/value)
valB=$(cat /sys/class/gpio/gpio$GPIOB/value)

if [ "$valA" == "1" ]; then
    GPIOA_text="HIGH"
else
    GPIOA_text="LOW"
fi

if [ "$valB" == "1" ]; then
    GPIOB_text="HIGH"
else
    GPIOB_text="LOW"
fi
echo "$GPIOA:$GPIOA_text  $GPIOB:$GPIOB_text"
echo 1 1>&2