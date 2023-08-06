from adsocket_transport.exceptions import ADSocketException


class ADSocketDuplicityError(ADSocketException):
    pass


class ADSocketConfigurationError(ADSocketException):
    pass
