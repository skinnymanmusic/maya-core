"""
OMEGA Core v3.0 - Test Fixtures
"""
from typing import Dict, Any
from datetime import datetime, timezone


def create_mock_pubsub_message() -> Dict[str, Any]:
    """Create mock Pub/Sub message for testing"""
    return {
        "message": {
            "data": "base64_encoded_data",
            "messageId": "test-message-id",
            "publishTime": datetime.now(timezone.utc).isoformat(),
        },
        "subscription": "test-subscription",
    }


def create_mock_gmail_message() -> Dict[str, Any]:
    """Create mock Gmail message for testing"""
    return {
        "id": "test-gmail-id",
        "threadId": "test-thread-id",
        "snippet": "Test email snippet",
    }

