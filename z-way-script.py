#!/usr/bin/env python3
## Author: Victor Nilsson
import os
import sys
import requests
import argparse
import json
import time

##
## Variables
##

# IP to z-way server. Change if needed
host = "http://172.26.135.1:8083"
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

def print_devices_title(devices):
        index=0
        for entry in devices:
                print("ID:" + str(index) + " -  " + entry["metrics"]["title"])
                index+=1


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
        
        #### Find binary switch devices connected to z-way controller.
        switch_device = []
        data = get_request(session, "devices")
        print("Devices available:")
        for device in data["data"]["devices"]:
                if device["deviceType"] == "switchBinary":
                        switch_device.append(device)
        
        #### Print devices and let user input loop sleep timings.
        print_devices_title(switch_device)
        input_nbr = int(input("Enter ID number of the borrowed switch (ID on the left): "))
        print("Configure loop timings (in seconds): ")
        sleep_on_time = int(input("Time switch will be ON: "))
        sleep_off_time = int(input("Time switch will be OFF: "))
        
        runtime=0
        iterations=0
        while True:
                print("On: ")
                print(get_request(session, "devices/" + switch_device[input_nbr]["id"] + "/command/on"))
                time.sleep(sleep_on_time)
                runtime+=sleep_on_time
                print("Off: ")
                print(get_request(session, "devices/" + switch_device[input_nbr]["id"] + "/command/off"))
                time.sleep(sleep_off_time)
                runtime+=sleep_off_time
                iterations+=1
                print("Running for ~" + str(runtime) + " seconds, " + str(iterations) + "on/off iterations")


if __name__ == "__main__":
    main(sys.argv[1:])



