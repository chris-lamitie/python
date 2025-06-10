#!/usr/bin/env python3
####################################################################
# CG Lamitie
# check_time_sync_50ms_alert.py
#
# Basic time checking script. Outputs to stdout, prints alert if time
# is off by +/- 50ms
#  
####################################################################

import subprocess
import datetime
import re

OFFSET_THRESHOLD_SEC = 0.050  # 50 milliseconds

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

def parse_offset(offset_str):
    match = re.match(r'([+-]?\d+\.\d+)\s+seconds', offset_str)
    return float(match.group(1)) if match else None

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

    offset_value = None
    if 'Last offset' in tracking_data:
        offset_str = tracking_data['Last offset']
        offset_value = parse_offset(offset_str)
        print(f"\nTime offset from NTP source: {offset_str}")
    if 'System time' in tracking_data:
        print(f"System time status: {tracking_data['System time']}")
    if 'Leap status' in tracking_data:
        print(f"Leap status: {tracking_data['Leap status']}")

    # Check for alert
    if offset_value is not None:
        if abs(offset_value) > OFFSET_THRESHOLD_SEC:
            print(f"\n⚠️ ALERT: Time offset exceeds ±{OFFSET_THRESHOLD_SEC:.3f}s! Offset = {offset_value:.6f}s")
        else:
            print(f"\n✅ Time offset is within acceptable range (±{OFFSET_THRESHOLD_SEC:.3f}s).")

if __name__ == "__main__":
    main()

