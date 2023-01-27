import serial
import time
import os

ser=serial.Serial('/dev/rfcomm0')
print(ser.isOpen())
ser.write(b'Enter Username:')
ssid=str(ser.readline())
ssid=ssid[2:len(ssid)-5]
ser.write(b'\n Enter Password:')
pwd=str(ser.readline())
pwd=pwd[2:len(pwd)-5]
print(ssid,pwd)
ser.write(b'Connecting.......')
print('Proceeding to connect')

interface='wlan0'
os.system('iwconfig '+interface+' essid '+ssid+' key '+pwd)
def CreateWifiConfig(SSID, password):
    config_lines = [
        'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
        'update_config=1',
        'country=US',
        '\n',
        'network={',
        '\tssid="{}"'.format(SSID),
        '\tpsk="{}"'.format(password),
        '}'
        ]
    config = '\n'.join(config_lines)
    print(config)
    #os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
        wifi.write(config)
    print("wifi config added")
CreateWifiConfig(ssid, pwd)
os.popen("sudo wpa_cli -i wlan0 reconfigure")