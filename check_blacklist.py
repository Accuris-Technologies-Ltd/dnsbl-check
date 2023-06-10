import asyncio
import pydnsbl
import logging
from netaddr import IPNetwork
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# SMTP email settings
sender_email = "your-email@example.com"
receiver_email = "receiver-email@example.com"
smtp_server = "smtp.example.com"
smtp_port = 587  # typically 587, 465, or 25
smtp_username = "smtp-username"
smtp_password = "smtp-password"

ip_list = ['192.0.2.0/24', '203.0.113.0/24']

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging to file
logging.basicConfig(filename=os.path.join('logs', f'blacklist_check_{datetime.now().strftime("%Y%m%d")}.log'), 
                    level=logging.INFO, 
                    format='%(asctime)s %(message)s')

def send_email_notification(blacklisted_ips):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Blacklisted IP Alert'
    body = '\n'.join([f"IP {ip} is blacklisted on: {', '.join(detected_by)}" for ip, detected_by in blacklisted_ips])
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # secure the connection
    server.login(smtp_username, smtp_password)  # login with mail_id and password
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

async def check_single_ip(ip_checker, single_ip, blacklisted_ips):
    result = await ip_checker.check_async(str(single_ip))
    if result.blacklisted:
        message = f"IP {single_ip} is blacklisted on: {', '.join(result.detected_by)}"
        print(message)
        logging.info(message)
        blacklisted_ips.append((str(single_ip), result.detected_by))
    else:
        message = f"IP {single_ip} is not blacklisted."
        print(message)
        logging.info(message)

async def check_ip_blacklist(ip_list):
    ip_checker = pydnsbl.DNSBLIpChecker()
    blacklisted_ips = []

    tasks = []
    for ip in ip_list:
        for single_ip in IPNetwork(ip):
            tasks.append(check_single_ip(ip_checker, single_ip, blacklisted_ips))
    await asyncio.gather(*tasks)

    # If we found any blacklisted IPs, send an email
    if blacklisted_ips:
        send_email_notification(blacklisted_ips)

# Run the asynchronous function
asyncio.run(check_ip_blacklist(ip_list))
