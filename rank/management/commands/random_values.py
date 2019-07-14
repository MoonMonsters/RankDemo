from django.core.management.base import BaseCommand
from rank.models import Username
from faker import Faker

faker = Faker(locale='en_US')


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(1000):
            try:
                Username.objects.create(name=faker.name())
            except:
                import traceback
                traceback.print_exc()
