class EntraAuthException(Exception):
    """Base exception for anything going wrong in the Entra auth flow."""


class TokenError(EntraAuthException):
    """Raised when MSAL / Graph returns an error payload for a token request."""

    def __init__(self, message, description):
        self.message = message or ""
        self.description = description or ""

    def __str__(self):
        return f"{self.message}\n{self.description}"


class FlowError(EntraAuthException):
    """Raised when the auth-code flow can't be found/resumed from the session."""

    def __init__(self, message):
        self.message = message or ""

    def __str__(self):
        return self.message
