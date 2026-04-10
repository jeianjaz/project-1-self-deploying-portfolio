import json
import boto3
import os
from datetime import datetime, timedelta

ce_client = boto3.client("ce")


def lambda_handler(event, context):
    today = datetime.utcnow().date()
    first_of_month = today.replace(day=1)

    try:
        # Get current month's cost
        response = ce_client.get_cost_and_usage(
            TimePeriod={
                "Start": first_of_month.strftime("%Y-%m-%d"),
                "End": today.strftime("%Y-%m-%d"),
            },
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[
                {"Type": "DIMENSION", "Key": "SERVICE"}
            ],
        )

        # Parse the cost data
        services = []
        total_cost = 0.0

        if response["ResultsByTime"]:
            for group in response["ResultsByTime"][0].get("Groups", []):
                service_name = group["Keys"][0]
                amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
                if amount > 0.001:
                    services.append({
                        "service": service_name,
                        "cost": round(amount, 4),
                    })
                    total_cost += amount

        services.sort(key=lambda x: x["cost"], reverse=True)

        result = {
            "period": f"{first_of_month.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}",
            "total_cost": round(total_cost, 4),
            "currency": "USD",
            "services": services[:10],
            "message": "Free tier target: $0.00" if total_cost < 0.01 else f"Current spend: ${round(total_cost, 2)}",
        }

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "Content-Type": "application/json",
            },
            "body": json.dumps(result),
        }

    except Exception as e:
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "period": "N/A",
                "total_cost": 0,
                "currency": "USD",
                "services": [],
                "message": f"Cost data unavailable: {str(e)}",
            }),
        }