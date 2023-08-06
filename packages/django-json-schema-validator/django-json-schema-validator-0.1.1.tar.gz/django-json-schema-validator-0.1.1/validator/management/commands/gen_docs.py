from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from validator.utils import SchemaLoader


class Command(BaseCommand):
    help = 'Generates api documentation based on schema.json'

    def add_arguments(self, parser):
        parser.add_argument('--apps', nargs='+', type=str)

    def handle(self, *args, **options):
        schema = SchemaLoader(settings.SCHEMA, settings.DOCUMENTATION)
        schema.generate_doc()
