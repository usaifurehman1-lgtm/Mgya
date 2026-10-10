import os
import requests


BUILD_SERVICE_URL = os.getenv(
    "BUILD_SERVICE_URL", ""
).strip()

BUILD_SERVICE_TOKEN = os.getenv(
    "BUILD_SERVICE_TOKEN", ""
).strip()


def check_build_service():
    if not BUILD_SERVICE_URL:
        return {
            "connected": False,
            "message": (
                "Build service URL is not configured."
            )
        }

    headers = {}

    if BUILD_SERVICE_TOKEN:
        headers["Authorization"] = (
            f"Bearer {BUILD_SERVICE_TOKEN}"
        )

    try:
        response = requests.get(
            BUILD_SERVICE_URL,
            headers=headers,
            timeout=15
        )

        return {
            "connected": response.ok,
            "http_status": response.status_code,
            "message": (
                "Service responded."
                if response.ok
                else "Service returned an error."
            )
        }

    except requests.RequestException:
        return {
            "connected": False,
            "message": (
                "Could not reach the build service."
            )
        }