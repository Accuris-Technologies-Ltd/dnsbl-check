# DNSBL IP Checker

This project is a Python script that checks a list of IPv4 addresses to see if they are blacklisted on any DNS-based Blackhole List (DNSBL) providers. The script logs the results of the checks and sends an email notification if any of the IPs are blacklisted.

## Prerequisites

Before running the script, ensure you have the following Python packages installed:

- asyncio
- pydnsbl
- netaddr
- smtplib
- email.mime.multipart
- email.mime.text
- logging

You can install these packages using pip:

```bash
pip install asyncio pydnsbl netaddr
```

The `smtplib`, `email.mime.multipart`, `email.mime.text`, and `logging` modules are part of the Python Standard Library and do not require separate installation.

## Configuration

Before running the script, replace the placeholders in the SMTP email settings and IP list with your actual data:

```python
# SMTP email settings
sender_email = "your-email@example.com"
receiver_email = "receiver-email@example.com"
smtp_server = "smtp.example.com"
smtp_port = 587  # typically 587, 465, or 25
smtp_username = "smtp-username"
smtp_password = "smtp-password"

# IP list
ip_list = ['192.0.2.0/24', '203.0.113.0/24']
```

- `sender_email` - The email from which you want to send the notification
- `receiver_email` - The email to which you want to send the notification
- `smtp_server` - The SMTP server of your email provider
- `smtp_port` - The SMTP port of your email provider
- `smtp_username` - The username for the SMTP server
- `smtp_password` - The password for the SMTP server
- `ip_list` - The list of IP addresses or ranges you want to check. The IPs should be provided as strings in standard IPv4 format or CIDR notation.

Make sure that the sender email is allowed to send emails via the specified SMTP server.

## Notice about DNS settings

Please ensure your system's DNS settings do not use Cloudflare or Quad9 DNS resolvers as these services are commonly blocked by the DNS-based Blackhole List (DNSBL) providers which are used by this script. You can check your DNS settings in the network settings of your operating system.

## Usage

To run the script, simply execute it with Python:

```bash
python check_blacklist.py
```

The script logs the results of the checks into a file in the 'logs' directory. The log files are named in the format 'blacklist_check_YYYYMMDD.log'. If any blacklisted IPs are found, an email notification is sent to the receiver email specified in the SMTP email settings.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
