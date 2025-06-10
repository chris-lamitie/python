#!/usr/bin/env python3
####################################################################
# CG Lamitie
# check_time_sync_basic.py
#
# Basic time checking script. Outputs to stdout
#  
####################################################################
import subprocess
import datetime

def get_system_time():
    return datetime.datetime.now()

def get_chrony_sources():
    try:
        output = subprocess.check_output(['chronyc', 'sources'], stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error running chronyc sources: {e.output.decode('utf-8')}"

def get_tracking_info():
    try:
        output = subprocess.check_output(['chronyc', 'tracking'], stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error running chronyc tracking: {e.output.decode('utf-8')}"

def parse_tracking_output(tracking_output):
    lines = tracking_output.splitlines()
    data = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()
    return data

def main():
    print("=== System Time Check ===")
    print(f"Local system time: {get_system_time()}")

    print("\n=== chronyc tracking ===")
    tracking = get_tracking_info()
    print(tracking)

    print("\n=== chronyc sources ===")
    sources = get_chrony_sources()
    print(sources)

    tracking_data = parse_tracking_output(tracking)
    if 'Last offset' in tracking_data:
        print(f"\nTime offset from NTP source: {tracking_data['Last offset']}")
    if 'System time' in tracking_data:
        print(f"System time status: {tracking_data['System time']}")
    if 'Leap status' in tracking_data:
        print(f"Leap status: {tracking_data['Leap status']}")

if __name__ == "__main__":
    main()
