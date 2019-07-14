from django.db import models


class Username(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class RankData(models.Model):
    value = models.CharField(max_length=32)
    count = models.IntegerField(default=0)
    cache_date = models.DateField(null=False)

    def __str__(self):
        return f'{self.value}:{self.count}'
