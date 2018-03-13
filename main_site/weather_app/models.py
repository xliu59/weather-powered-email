from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=200)
    population = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    state = models.CharField(max_length=200)
    state_abbr = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.city_name


class Subscriber(models.Model):
    email = models.CharField(max_length=200, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.email