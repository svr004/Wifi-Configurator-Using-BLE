import serial
import subprocess
import os

def get_connected_device_mac():
    try:
        result = subprocess.run(['bluetoothctl', 'info'], stdout=subprocess.PIPE, text=True)
        output = result.stdout
        
        mac_address = None
        for line in output.split('\n'):
            if 'Device' in line:
                mac_address = line.split(' ')[1]
            if 'Connected: yes' in line and mac_address:
                print(f"Connected device MAC address: {mac_address}")
                return mac_address
        
        print("No connected devices found.")
    except subprocess.CalledProcessError as e:
        print(f"Error running bluetoothctl: {e}")
    return None

def open_serial_port(port='/dev/rfcomm0', baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate)
        if ser.isOpen():
            print(f"Serial port {port} opened successfully.")
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        return None

def read_from_serial(ser, prompt):
    ser.write(prompt.encode())
    response = ser.readline().decode().strip()
    return response

def create_wifi_config(ssid, password):
    config_lines = [
        'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
        'update_config=1',
        'country=US',
        '',
        'network={',
        f'\tssid="{ssid}"',
        f'\tpsk="{password}"',
        '}'
    ]
    return '\n'.join(config_lines)

def write_wifi_config(config, filepath="/etc/wpa_supplicant/wpa_supplicant.conf"):
    try:
        with open(filepath, "w") as wifi:
            wifi.write(config)
        print("WiFi configuration written successfully.")
    except PermissionError as e:
        print(f"Permission error writing WiFi configuration: {e}")

def reconfigure_wifi(interface='wlan0'):
    try:
        subprocess.run(["sudo", "wpa_cli", "-i", interface, "reconfigure"], check=True)
        print("WiFi reconfigured successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error reconfiguring WiFi: {e}")

def main():
    mac_address = get_connected_device_mac()
    if not mac_address:
        print("No connected Bluetooth device found.")
        return

    ser = open_serial_port()
    if not ser:
        print("No serial connection could be established.")
        return

    ssid = read_from_serial(ser, 'Enter Username: ')
    pwd = read_from_serial(ser, 'Enter Password: ')
    print(f"Received SSID: {ssid}, Password: {pwd}")

    ser.write(b'Connecting.......')
    wifi_config = create_wifi_config(ssid, pwd)
    print(wifi_config)

    write_wifi_config(wifi_config)
    reconfigure_wifi()

if __name__ == "__main__":
    main()
