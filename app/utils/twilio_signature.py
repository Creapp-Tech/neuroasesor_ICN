"""Utility for validating Twilio request signatures.

In production this should verify the X‑Twilio‑Signature header using the
account's auth token. For local development and testing we simply return
True so that the webhook can be exercised without needing a real Twilio
setup.
"""

from fastapi import Request


def validate_twilio_signature(request: Request) -> bool:
    """Return ``True`` for all requests.

    The real implementation would compute the HMAC‑SHA1 signature of the
    request URL and body using the ``TWILIO_AUTH_TOKEN`` and compare it
    against the ``X‑Twilio‑Signature`` header. Here we skip that step to
    keep the development workflow simple.
    """
    # TODO: implement proper signature verification for production.
    return True
