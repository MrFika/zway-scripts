#!/usr/bin/env python3
import os
import sys
import requests
import argparse
import json
import time

##
## Variables
##

# Change the IP!
host = "http://192.168.1.134:8083"
api_path = "/ZAutomation/api/v1/"


##
## Functions
##

def get_request(session, command):
    req = session.get(host + api_path + command)
    return req.json()

def post_request(session, command, post_data):
    req = session.post(host + api_path + command, data=post_data)
    return req.json()

def login_request(session, login_header, login_payload):
	resp = session.post(host + api_path + 'login', headers=login_header, json=login_payload)
	return resp.status_code

##
## Main Program
##
    
def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument("username", help="Username", type=str)
	parser.add_argument("password", help="Password", type=str)
	args = parser.parse_args()

	
	#### Do the Login.
	login_payload = {"login": args.username, "password": args.password, "rememberme": 'true'}
	login_header = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json;charset=utf-8'}
	
	session = requests.Session()
	if (login_request(session, login_header, login_payload)!=200):
		print("Failed to login")
		sys.exit()
	
	switch_device = []
	data = get_request(session, "devices")
	for device in data["data"]["devices"]:
		if device["deviceType"] == "switchBinary":
			## Could be modified to use a manually assigned ID.
			title = device["metrics"]["title"] 
			switch_device.append(device)
	
	input_nbr = int(input("Enter switch Number: "))
	sleep_on_time = int(input("Time switch will be ON: "))
	sleep_off_time = int(input("Time switch will be OFF: "))
	while True:
		print("On: ")
		print(get_request(session, "devices/" + switch_device[input_nbr]["id"] + "/command/on"))
		time.sleep(sleep_on_time)
		print("Off: ")
		print(get_request(session, "devices/" + switch_device[input_nbr]["id"] + "/command/off"))
		time.sleep(sleep_off_time)


if __name__ == "__main__":
    main(sys.argv[1:])



