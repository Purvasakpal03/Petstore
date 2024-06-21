from django.db import models

# Create your models here.
class pet(models.Model):
    gender=(("MALE","male"),("FEMALE","female"))
    image=models.ImageField(upload_to="media")
    name=models.CharField(max_length=200)
    species=models.CharField(max_length=200)
    breed=models.CharField(max_length=200)
    age=models.IntegerField()
    gender=models.CharField(max_length=200,choices=gender)
    description=models.CharField(max_length=500)
    price=models.FloatField()

    class Meta:
        db_table="pet"

class customer(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    phoneno=models.BigIntegerField()
    password=models.CharField(max_length=200)

    class Meta:
        db_table="customer"