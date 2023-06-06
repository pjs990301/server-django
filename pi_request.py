import requests
import subprocess
import json

serial = subprocess.check_output('cat /proc/cpuinfo | grep Serial | awk \'{print $3}\'', shell=True)
serial = serial.decode('utf-8')

iwconfig = subprocess.check_output('ifconfig wlan0', shell=True)
iwconfig = iwconfig.decode('utf-8')
bssid = ""

# Python3 Version
# index = iwconfig.decode.find("Access Point: ")

# Python2 Version

index = iwconfig.find("ether ")
for i in range(index+6, index + 25):
    bssid += iwconfig[i]
bssid = bssid.upper()

# serial=serial+"test"
# bssid = bssid+"test"
# url = "http://blue-sun.kro.kr:9000/pi/"
url = "http://3.37.161.170:8000/pi/"
data = {
    "serial_number": serial,
    "mac_address": bssid,
    "type": 1
}
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
requests.post(url, data=json.dumps(data), headers=headers)
