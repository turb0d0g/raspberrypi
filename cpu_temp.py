import gpiozero as gpz

cpu = gpz.CPUTemperature()
cpu_temp = cpu.temperature
print(cpu_temp)
