from django.db import models

# Create your models here.
class Taskapp(models.Model):
    name=models.CharField(max_length=300)
    description=models.CharField(max_length=300)
    status=models.CharField(max_length=300)

    class Meta:
        db_table='Taskapp'
