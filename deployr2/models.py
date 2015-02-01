from django.db import models

# Create your models here.


class Deployment(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    create_date = models.DateTimeField()
    # TODO backend, frontend branch
    # TODO backend, frontend build
    # TODO status. Or should we always get this from docker?
    # TODO creator