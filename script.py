import os
import whois
from datetime import datetime
import requests
import json
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_mattermost_notification(webhook_url, message):
    payload = {"text": message}
    try:
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        response.raise_for_status()
        print("Notification sent to Mattermost successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification to Mattermost: {e}")


def check_domain_availability(domain, webhook_url):
    try:
        domain_info = whois.whois(domain)
        current_date = datetime.now()

        if domain_info.domain_name:
            # py-lint: disable=C0301
            message = f"📅 {current_date.strftime('%Y-%m-%d %H:%M:%S')}: {domain} is still registered."
        else:
            message = f"🎉 {current_date.strftime('%Y-%m-%d %H:%M:%S')}: The domain {domain} is now available!"

        print(message)
        send_mattermost_notification(webhook_url, message)

    except whois.parser.PywhoisError:
        message = f"❗ {current_date.strftime('%Y-%m-%d %H:%M:%S')}: An error occurred while checking {domain}. It might be available."
        print(message)
        send_mattermost_notification(webhook_url, message)


if __name__ == "__main__":
    domain = os.environ.get("DOMAIN")
    webhook_url = os.environ.get("WEBHOOK_URL")
    if not domain:
        logger.error("Error: DOMAIN environment variable is not set.")
        sys.exit(1)
    if not webhook_url:
        logger.error("Error: WEBHOOK_URL environment variable is not set.")
        sys.exit(1)

    check_domain_availability(domain, webhook_url)
