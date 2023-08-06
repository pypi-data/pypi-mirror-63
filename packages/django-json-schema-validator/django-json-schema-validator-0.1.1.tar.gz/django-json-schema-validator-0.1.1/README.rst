Validator
=========

Validator is a Django app used to validate request and response objects for django apis.

Quick start
-----------

1. Add "validator" to your INSTALLED_APPS setting like this before your apps::

    INSTALLED_APPS = [
        ...
        'validator',
    ]

2. Add "validator.middleware.Validator" to your MIDDLEWARE setting like this::

    MIDDLEWARE = [
        ...
        'validator.middleware.Validator',
        'django.middleware.common.CommonMiddleware',
        ...
    ]

3. Add SCHEMA variable in settings.py, which gives the location of the schema.json file.

    SCHEMA = 'ext_app/schema.json'
   
4. Add DOCUMENTATION variable in settings.py, which gives the location of the DOC.md file to be generated.

    DOCUMENTATION = 'ext_app/DOC.md'

5. To generate api documentation from schema.json, run

   ``python3 manage.py gen_docs``

