from django.core.management.base import BaseCommand
from rank.models import Username
from faker import Faker

faker = Faker(locale='en_US')


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(100):
            try:
                name = Username.objects.create(name=faker.name())
                print('>>>name = ' + str(name))
            except:
                import traceback
                traceback.print_exc()
