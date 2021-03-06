from datetime import datetime, timedelta


def datetime_in_n_seconds(seconds: int = 0) -> datetime:
    """
    Return the datetime object for n seconds in the future.

    :param seconds: How many seconds to add on.
    """
    return datetime.now() + timedelta(seconds=seconds)


class OAuthToken:
    def __init__(self, token: str = "", expiry: datetime = datetime.now() - timedelta(1)):
        self.token = token
        self.expiry = expiry

    def token_valid(self) -> bool:
        """
        Return whether or not there is at least 45 seconds of token lifespan left.
        """
        return datetime_in_n_seconds(seconds=45) < self.expiry
