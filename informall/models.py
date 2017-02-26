from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(max_length=1000, blank=True)
    description = models.TextField(null=True)
    permissions = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.name

class Library(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    state = models.ForeignKey('State', blank=True, null=True)
    institution_type = models.CharField(max_length=100, default='public', choices=(('public','public'),('academic','academic'),('private','private')))
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
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
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    state = models.ForeignKey('State', blank=True, null=True)

    def __unicode__(self):
        return self.name
