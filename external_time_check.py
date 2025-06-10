#!/usr/bin/env python3
####################################################################
# CG Lamitie
# check_time_sync.py
#
# Time checking script that checks local system time against an external
# ntp source. Sends results to stdout, rsysclog, and email.
#  
####################################################################
import ntplib
import time
import subprocess
import socket
from datetime import datetime

# Configuration
NTP_SERVER = 'pool.ntp.org'
TIME_THRESHOLD = 0.050  # in seconds
ALERT_EMAIL = 'admin@example.com'
HOSTNAME = socket.gethostname()

def log_to_syslog(message):
    subprocess.run(['logger', '-t', 'TimeSyncCheck', message])

def send_email_alert(offset, system_time, ntp_time):
    subject = f"ALERT: {HOSTNAME} time offset exceeds 50ms threshold"
    body = (
        f"Hostname    : {HOSTNAME}\n"
        f"Issue       : System time offset exceeded threshold of 50ms.\n\n"
        f"Offset      : {offset:.6f} seconds\n"
        f"System Time : {datetime.fromtimestamp(system_time)}\n"
        f"NTP Time    : {datetime.fromtimestamp(ntp_time)}\n"
    )
    subprocess.run(
        ['mail', '-s', subject, ALERT_EMAIL],
        input=body.encode(),
        check=False
    )

def check_time_accuracy():
    try:
        client = ntplib.NTPClient()
        response = client.request(NTP_SERVER, version=3)

        system_time = time.time()
        ntp_time = response.tx_time
        offset = abs(system_time - ntp_time)

        log_message = (
            f"{HOSTNAME} - System Time: {datetime.fromtimestamp(system_time)}, "
            f"NTP Time: {datetime.fromtimestamp(ntp_time)}, "
            f"Offset: {offset:.6f}s"
        )
        print(log_message)
        log_to_syslog(log_message)

        if offset <= TIME_THRESHOLD:
            print("✅ System time is within 50ms of the NTP server.")
        else:
            print("❌ System time is NOT within 50ms of the external NTP server.")
            log_to_syslog("Time offset exceeded 50ms threshold.")
            send_email_alert(offset, system_time, ntp_time)

    except Exception as e:
        error_message = f"{HOSTNAME} - Error validating system time: {e}"
        print(error_message)
        log_to_syslog(error_message)

if __name__ == "__main__":
    check_time_accuracy()
