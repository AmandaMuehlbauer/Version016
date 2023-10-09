from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

class Command(BaseCommand):
    help = 'Check if Elasticsearch is working properly'

    def handle(self, *args, **options):
        try:
            # Replace with your Elasticsearch configuration (e.g., host and port)
            es = Elasticsearch(hosts=['jidder-elasticsearch:9300'])

            # Check if Elasticsearch is up and running
            if es.ping():
                self.stdout.write(self.style.SUCCESS('Elasticsearch is working properly!'))
            else:
                self.stdout.write(self.style.ERROR('Elasticsearch is not responding to ping.'))
        except ConnectionError:
            self.stdout.write(self.style.ERROR('Unable to connect to Elasticsearch. Check your configuration.'))
