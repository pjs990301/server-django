import requests
import subprocess
import json


serial = subprocess.check_output('cat /proc/cpuinfo | grep Serial | awk \'{print $3}\'', shell=True)

iwconfig = subprocess.check_output('iwconfig wlan0',shell=True)
bssid = ""
index = iwconfig.find("Access Point: ")
for i in range(index + 14,index + 31): 
    bssid +=iwconfig[i]

url = "http://blue-sun.kro.kr:9000/pi/"
data = {
	"serial_number" : serial, 
	"mac_address" : bssid, 
	"type" : 1
	}
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
requests.post(url, data=json.dumps(data), headers=headers)