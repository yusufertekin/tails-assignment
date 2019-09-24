from django.core.management.base import BaseCommand

from tails.utils import load_stores


class Command(BaseCommand):
    help = 'Load stores from stores.json file'

    def handle(self, *args, **options):
        load_stores()
        self.stdout.write('Saved stores')
