import binascii
import warnings

from openapi_core.security.exceptions import SecurityError
from openapi_core.security.util import b64decode


class BaseProvider(object):

    def __init__(self, scheme):
        self.scheme = scheme


class UnsupportedProvider(BaseProvider):

    def __call__(self, request):
        warnings.warn("Unsupported scheme type")


class ApiKeyProvider(BaseProvider):

    def __call__(self, request):
        source = getattr(request.parameters, self.scheme.apikey_in.value)
        if self.scheme.name not in source:
            raise SecurityError("Missing api key parameter.")
        return source.get(self.scheme.name)


class HttpProvider(BaseProvider):

    def __call__(self, request):
        if 'Authorization' not in request.parameters.header:
            raise SecurityError('Missing authorization header.')
        auth_header = request.parameters.header['Authorization']
        try:
            auth_type, encoded_credentials = auth_header.split(' ', 1)
        except ValueError:
            raise SecurityError('Could not parse authorization header.')

        if auth_type.lower() != self.scheme.scheme.value:
            raise SecurityError(
                'Unknown authorization method %s' % auth_type)
        try:
            return b64decode(encoded_credentials).decode('latin1')
        except binascii.Error:
            raise SecurityError('Invalid base64 encoding.')
