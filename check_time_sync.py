#!/usr/bin/env python3
####################################################################
# CG Lamitie
# check_time_sync.py
#
# Time checking script that sends results to local logger and email.
# For chronyd systems.
#  
####################################################################
import subprocess
import datetime
import re
import smtplib
import socket
from email.message import EmailMessage

# === Configuration ===
OFFSET_THRESHOLD_SEC = 0.050
EMAIL_FROM = "timesync-alert@yourdomain.com"
EMAIL_TO = "youremail@yourdomain.com"
SYSLOG_TAG = "timesync-check"

def log_to_syslog(message, level="info"):
    try:
        subprocess.run(
            ["logger", f"--tag={SYSLOG_TAG}", f"--priority=user.{level}", message],
            check=True
        )
    except Exception as e:
        print(f"Failed to log to syslog: {e}")

def check_chronyd_status():
    try:
        result = subprocess.run(['systemctl', 'is-active', 'chronyd'], capture_output=True, text=True, check=True)
        status = result.stdout.strip()
        return status == "active"
    except subprocess.CalledProcessError as e:
        return False

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

def send_email_alert(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg.set_content(body)
    try:
        with smtplib.SMTP('localhost') as server:
            server.send_message(msg)
        log_to_syslog(f"Alert email sent to {EMAIL_TO}", "warning")
    except Exception as e:
        log_to_syslog(f"Failed to send alert email: {e}", "error")

def main():
    hostname = socket.gethostname()
    now = datetime.datetime.now()

    if not check_chronyd_status():
        msg = (
            f"❌ chronyd service is NOT running on {hostname}!\n"
            f" Time: {now}\n"
            f" This may result in inaccurate time on the system!\n"
        )
        subject = f"❌ chronyd Down on {hostname}"
        log_to_syslog(msg.strip(), "error")
        send_email_alert(subject, msg)
        return  # No point continuing if chronyd is down

    tracking = get_tracking_info()
    sources = get_chrony_sources()
    tracking_data = parse_tracking_output(tracking)

    offset_str = tracking_data.get('Last offset', 'unknown')
    offset_val = parse_offset(offset_str)

    log_to_syslog(f"System time check at {now}", "info")
    log_to_syslog(f"Last offset: {offset_str}", "info")

    if offset_val is not None:
        if abs(offset_val) > OFFSET_THRESHOLD_SEC:
            alert_msg = (
                f"⚠️ Time offset exceeded threshold on {hostname}!\n"
                f" Time: {now}\n"
                f" Offset: {offset_val:.6f}s\n"
                f" Threshold: ±{OFFSET_THRESHOLD_SEC:.3f}s\n"
            )
            full_email = (
                f"{alert_msg}\n"
                f"--- Tracking Info ---\n{tracking}\n"
                f"--- Sources ---\n{sources}"
            )
            subject = f"⚠️ Time Sync Alert on {hostname}"
            log_to_syslog(alert_msg.strip(), "warning")
            send_email_alert(subject, full_email)
        else:
            log_to_syslog(f"✅ Offset {offset_val:.6f}s within threshold (±{OFFSET_THRESHOLD_SEC:.3f}s)", "info")
    else:
        log_to_syslog("❌ Unable to parse offset from chrony tracking output", "error")

if __name__ == "__main__":
    main()
