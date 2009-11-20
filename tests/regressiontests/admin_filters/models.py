from django.db import models
from django.contrib.sites.models import Site

class Filterable(models.Model):
    sites = models.ManyToManyField(Site, blank=True)


from django.contrib import admin

class FilterableAdmin(admin.ModelAdmin):
    list_filter = ('sites__domain',)

admin.site.register(Filterable, FilterableAdmin)

