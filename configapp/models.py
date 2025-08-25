from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=150)
    year = models.IntegerField()
    photo = models.ImageField(upload_to='photos/%Y/%m%d/', null=True, blank=True)
    genre = models.CharField(max_length=50)
    actor = models.ManyToManyField('Actor')

    def __str__(self):
        return self.name
    
class Actor(models.Model):
    name = models.CharField(max_length=150)
    birthdate = models.DateField()

    def __str__(self):
        return self.name

