from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Library(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    state = models.ForeignKey('State', blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    resources = models.ManyToManyField(Resource, blank=True)

    def __unicode__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name

class News(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    newstype = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    state = models.ForeignKey('State', blank=True, null=True)

    def __unicode__(self):
        return self.name
