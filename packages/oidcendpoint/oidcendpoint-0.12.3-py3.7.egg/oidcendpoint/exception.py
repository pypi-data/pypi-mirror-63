class OidcEndpointError(Exception):
    pass


class InvalidRedirectURIError(OidcEndpointError):
    pass


class InvalidSectorIdentifier(OidcEndpointError):
    pass


class ConfigurationError(OidcEndpointError):
    pass


class NoSuchAuthentication(OidcEndpointError):
    pass


class TamperAllert(OidcEndpointError):
    pass


class ToOld(OidcEndpointError):
    pass


class MultipleUsage(OidcEndpointError):
    pass


class FailedAuthentication(OidcEndpointError):
    pass


class InstantiationError(OidcEndpointError):
    pass


class ImproperlyConfigured(OidcEndpointError):
    pass


class NotForMe(OidcEndpointError):
    pass


class UnknownAssertionType(OidcEndpointError):
    pass


class RedirectURIError(OidcEndpointError):
    pass


class UnknownClient(OidcEndpointError):
    pass


class InvalidClient(OidcEndpointError):
    pass


class UnAuthorizedClient(OidcEndpointError):
    pass


class InvalidCookieSign(Exception):
    pass


class OnlyForTestingWarning(Warning):
    "Warned when using a feature that only should be used for testing."
    pass


class ProcessError(OidcEndpointError):
    pass


class ServiceError(OidcEndpointError):
    pass


class InvalidRequest(OidcEndpointError):
    pass


class CapabilitiesMisMatch(OidcEndpointError):
    pass
