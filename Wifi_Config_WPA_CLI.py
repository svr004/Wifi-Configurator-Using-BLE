mport os
import time
from time import sleep
import subprocess
from subprocess import Popen, PIPE

def cnct(ssid,pwd):
    cm='wpa_cli add_network'
    stdout=Popen(cm,shell=True,stdout=PIPE).stdout
    #sleep(10)
    x=str(stdout.read())
    t=len(x)
    l=x[t-4 :t-3]
    l1=int(l)-1
    l=str(l1)
    print(l)
    subprocess.run(["wpa_cli", "set_network", l, "ssid", '\"' + ssid + '\"'])
    subprocess.run(["wpa_cli", "set_network", l, "psk", '\"' + pwd + '\"'])

    subprocess.run(["wpa_cli", "enable_network", l])
    subprocess.run(["wpa_cli", "save_config", l])
    os.popen("sudo wpa_cli -i wlan0 reconfigure")


cnct('ssid','pwd')
