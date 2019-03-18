import time

from django.db import connections
from django.db.utils import OperationalError

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause exec until db is available"""

    # handle function is the function that will be executed
    # whenever we run the management command
    def handle(self, *args, **options):
        self.stdout.write("Waiting for db...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('db unavailable waiting 1 sec')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('db is available!'))
