from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import json

from .utils import validate, load_schema, SchemaError, json_response


class Validator(MiddlewareMixin):
    def _locate_schema(self, schema, url):
        return schema[url] if url in schema else None

    def _validate(self, url, body, request_or_response):
        schema = load_schema(settings.SCHEMA)['schema']
        schema = self._locate_schema(schema, url)
        if not schema:
            return True, ''
        schema = schema[request_or_response]
        if isinstance(body, bytes):
            body = json.loads(body)
        try:
            validate(schema, body)
            return True, ''
        except SchemaError.ValidationError as e:
            return False, str(e)

    def process_request(self, request):
        validated, error = self._validate(request.path_info, request.body, 'request')
        if not validated:
            return json_response(error, 'request')

    def process_response(self, request, response):
        resp = json.loads(response._container[0].decode())
        validated, error = self._validate(request.path_info, resp, 'response')
        if not validated:
            return json_response(error, 'response')
        return response
