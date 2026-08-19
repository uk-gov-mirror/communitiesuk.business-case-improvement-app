import json


class EntraStateSerializer:
    """
    Round-trips small bits of app state (e.g. the `next` redirect URL)
    through Entra's OAuth `state` parameter. Entra passes `state` back
    to the callback unmodified, so we use it to remember where the user
    was trying to go before they were bounced to login.
    """

    def serialize(self, **kwargs) -> str:
        return json.dumps(kwargs)

    def deserialize(self, state: str) -> dict:
        try:
            return json.loads(state)
        except (json.JSONDecodeError, TypeError):
            return {}
