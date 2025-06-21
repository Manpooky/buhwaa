from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Language(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class VisaType(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    countries = models.ManyToManyField(Country, related_name='visa_types')
    
    def __str__(self):
        return self.name 