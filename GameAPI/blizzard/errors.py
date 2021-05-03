class BlizzardAPIException(Exception):
    pass


class BlizzardAPIQuotaException(BlizzardAPIException):
    pass


class BlizzardAPIUnmodifiedData(BlizzardAPIException):
    pass
