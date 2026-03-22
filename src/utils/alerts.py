import requests
import json

import os

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(message, dag_id=None, task_id=None, log_url=None):
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 Airflow Task Failed",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*DAG:*\n{dag_id}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Task:*\n{task_id}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Error Message:*\n```{message}```"
                }
            }
        ]
    }

    # Add log button if available
    if log_url:
        payload["blocks"].append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "🔍 View Logs"
                    },
                    "url": log_url
                }
            ]
        })

    requests.post(
        SLACK_WEBHOOK_URL,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )