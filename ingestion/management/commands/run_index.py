from django.core.management.base import BaseCommand
from ingestion.views import index

class Command(BaseCommand):
    help = 'Run the index view from the command line'

    def handle(self, *args, **kwargs):
        response = index(None)
        self.stdout.write(response.content.decode())
