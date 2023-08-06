import jsonschema
import json
from django.http import JsonResponse


def validate(schema, json):
    return jsonschema.validate(json, schema)


def load_schema(schema_path):
    return json.loads(open(schema_path).read())


class SchemaError:
    ValidationError = jsonschema.exceptions.ValidationError


class SchemaLoader:
    def __init__(self, schema_path, doc_path):
        self.schema = load_schema(schema_path)['schema']
        self.text = ''
        self.doc_path = doc_path
        self.file = open(doc_path, 'w')

    def _add_text(self, text):
        self.text += text

    def _write_url(self, url):
        self._add_text(f'''URL - `{url}`''')
        return self

    def _get_object_details(self, obj):
        props = dict()
        for prop, _type in obj['properties'].items():
            if _type['type'] == 'object':
                props[prop] = self._get_object_details(_type)['type']
            else:
                props[prop] = _type['type']
        return dict(type=props)

    def _get_request_or_response_object(self, request):
        required = request['required']
        properties = dict()
        for k, v in request['properties'].items():
            if v['type'] == 'object':
                v = self._get_object_details(v)
            properties[k if k in required else f'[, {k}]'] = v['type']
        return properties

    def _write_request_body(self, request):
        self._add_text(f'''Request''')
        self._add_text('''\n```\n''')
        properties = self._get_request_or_response_object(request)
        self._add_text(json.dumps(properties, indent=4))
        self._add_text('''\n```\n''')
        return self

    def _write_response_body(self, response):
        self._add_text(f'''Response''')
        self._add_text('''\n```\n''')
        properties = self._get_request_or_response_object(response)
        self._add_text(json.dumps(properties, indent=4))
        self._add_text('''\n```''')
        return self

    def _add_line_break(self):
        self._add_text('''\n''')
        return self

    def _add_separator(self):
        self._add_text('''===================================''')
        return self

    def _generate_doc(self):
        for url, doc in self.schema.items():
            self._write_url(url).\
                _add_line_break(). \
                _add_line_break(). \
                _write_request_body(doc['request']). \
                _add_line_break(). \
                _write_response_body(doc['response']). \
                _add_line_break().\
                _add_separator().\
                _add_line_break().\
                _add_line_break()

        self.file.write(self.text)
        self.file.close()
        print(f'Generated at {self.doc_path}')

    def generate_doc(self):
        self._generate_doc()


def json_response(error, error_type):
    return JsonResponse(dict(error=error, errot_type=error_type), status=400)
