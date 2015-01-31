from django.db import models

# Create your models here.


class Deployment(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    create_date = models.DateTimeField()