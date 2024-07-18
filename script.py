import os
import whois
from datetime import datetime
import requests
import json
import logging
import sys
import opsgenie_sdk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_alert_to_opsgenie(api_key, message, domain):
    """send alert to Opsgenie when domain is available"""
    configuration = opsgenie_sdk.Configuration()
    configuration.api_key["Authorization"] = api_key
    api_client = opsgenie_sdk.api_client.ApiClient(configuration)
    alert_api = opsgenie_sdk.AlertApi(api_client)
    body = opsgenie_sdk.CreateAlertPayload(
        message=message,
        description="Domain is available",
        priority="P1",
        alias=f"domain-availability-{domain}",
    )
    try:
        response = alert_api.create_alert(create_alert_payload=body)
        print("Alert sent to Opsgenie successfully.")
    except opsgenie_sdk.ApiException as e:
        print(f"Failed to send alert to Opsgenie: {e}")
        sys.exit(1)


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


def check_domain_availability(domain, webhook_url=None, opsgenie_api_key=None):
    try:
        domain_info = whois.whois(domain)
        expiration_date = domain_info.expiration_date
        # Parse to get delete date
        whois_text = domain_info.text
        delete_date = None
        for line in whois_text.split("\n"):
            if "Delete date:" in line:
                delete_date = line.split(":")[1].strip()
                break
        current_date = datetime.now()

        if domain_info.domain_name:
            # py-lint: disable=C0301
            message = f"📅 {current_date.strftime('%Y-%m-%d %H:%M:%S')}: {domain} is still registered. expires: {expiration_date}"
            if delete_date is not None:
                message += f" delete date: {delete_date}"
            logger.info(message)
            logger.debug(domain_info)
            if webhook_url is not None:
                send_mattermost_notification(webhook_url, message)
        else:
            message = f"🎉 {current_date.strftime('%Y-%m-%d %H:%M:%S')}: The domain {domain} is now available!"
            logger.info(message)
            if opsgenie_api_key is not None:
                send_alert_to_opsgenie(
                    opsgenie_api_key,
                    message,
                    domain,
                )
            if webhook_url is not None:
                send_mattermost_notification(webhook_url, message)

    except whois.parser.PywhoisError:
        message = f"❗ {current_date.strftime('%Y-%m-%d %H:%M:%S')}: An error occurred while checking {domain}. It might be available."
        print(message)
        send_mattermost_notification(webhook_url, message)


if __name__ == "__main__":
    opsgenie_api_key = os.environ.get("OPSGENIE_API_KEY") or None
    domain = os.environ.get("DOMAIN")
    webhook_url = os.environ.get("WEBHOOK_URL") or None
    if not domain:
        logger.error("Error: DOMAIN environment variable is not set.")
        sys.exit(1)
    check_domain_availability(domain, webhook_url, opsgenie_api_key)
