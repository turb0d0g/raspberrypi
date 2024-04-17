import os
import datetime
import subprocess
from pijuice import PiJuice


DIRECTORY = '//home/pi/uptest.txt'
COLUMNS= 'Date,Time_Stamp,Time_Up,Load_Average_1,Load_Average_2,Load_Average_3,Batt_Charge,Batt_Error'


PiJ = PiJuice(1, 0x14)
batt_charge_status_dict = (PiJ.status.GetChargeLevel())
batt_charge_val = str(batt_charge_status_dict.get('data'))
batt_error = batt_charge_status_dict.get('error')


current_time = str(datetime.datetime.now())

with open('/proc/uptime', 'r') as f:
         up_seconds = float(f.readline().split()[0])

hours = int(up_seconds//3600) # get number of hours
mins = int((up_seconds%3600)//60) # get number of minutes
seconds = ((up_seconds%3600)%60) # get number of seconds

uptime_str = str(hours)+':'+str(mins)+':'+str(round(seconds,2))

loadaverage = str(subprocess.check_output("uptime", stderr=subprocess.STDOUT, shell=True))[-33:-3]

info = (current_time+', '+uptime_str+', ' + loadaverage+', batt_charge_val: '+batt_charge_val+', batt_error: '+batt_error)
info_split = info.split()
info_to_upload = (info_split[0]+',', info_split[1], info_split[2], info_split[5], info_split[6],info_split[7], info_split[9], info_split[11])
info_to_upload = ''.join(info_to_upload) #tuple to string
info_to_upload = '\n'+info_to_upload

upfile = open(DIRECTORY, 'a')

if os.stat(DIRECTORY).st_size == 0:
    upfile.write(COLUMNS)

upfile.write(info_to_upload)
upfile.close()


