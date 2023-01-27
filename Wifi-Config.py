import os

def CreateWifiConfig(self,SSID, password):
        print('Here')
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
        os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
            wifi.write(config)
            print("wifi config added")


def main():
    x=str(input())
    y=str(input())

    CreateWifiConfig(x,y)
    os.popen("sudo wpa_cli -i wlan0 reconfigure")

if __name__=="__main__":

    main()

   