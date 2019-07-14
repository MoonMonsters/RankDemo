from django.core.management.base import BaseCommand
from djcelery.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    def handle(self, *args, **options):
        interval = IntervalSchedule.objects.filter(every=30, period='seconds').first()
        periodic_task = PeriodicTask(name='test', task='rank.tasks.interval_print', interval=interval)
        periodic_task.save()
