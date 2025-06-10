#!/usr/bin/env python3
####################################################################
# CG Lamitie
# check_time_sync.py
#
# Time checking script that checks local system time against an external
# ntp source. Sends results to stdout.
#  
####################################################################
import ntplib
import time
from datetime import datetime

# Threshold for acceptable time drift in seconds (50 milliseconds)
TIME_THRESHOLD = 0.050
NTP_SERVER = 'pool.ntp.org'

def check_time_accuracy():
    try:
        client = ntplib.NTPClient()
        response = client.request(NTP_SERVER, version=3)

        system_time = time.time()
        ntp_time = response.tx_time
        offset = abs(system_time - ntp_time)

        print(f"System Time       : {datetime.fromtimestamp(system_time)}")
        print(f"NTP Time          : {datetime.fromtimestamp(ntp_time)}")
        print(f"Time Difference   : {offset:.6f} seconds")

        if offset <= TIME_THRESHOLD:
            print("✅ System time is within 50ms of the NTP server.")
        else:
            print("❌ System time is NOT within 50ms of the NTP server.")
    except Exception as e:
        print(f"Error: Could not validate system time. Details: {e}")

if __name__ == "__main__":
    check_time_accuracy()

