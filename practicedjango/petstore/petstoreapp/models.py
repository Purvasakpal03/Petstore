from django.db import models
from django.db.models import Manager

# Create your models here.

class custommanger(models.Manager):
    def getdata(self,a):
        return super().get_queryset().filter(species=a)
    
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

        # cpetobj = custommanger()
        # objects = Manager()

class customer(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    phoneno=models.BigIntegerField()
    password=models.CharField(max_length=200)

    class Meta:
        db_table="customer"

class cart(models.Model):
    cid = models.ForeignKey(customer,on_delete=models.CASCADE)
    pid = models.ForeignKey(pet,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    totalamount= models.FloatField()

    class Meta:
        db_table='cart'

class order(models.Model):
    ordernumber=models.CharField(max_length=200)
    orderdate=models.DateField()
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    phoneno=models.BigIntegerField()
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    pincode=models.IntegerField()
    orderstatus=models.CharField(max_length=200)

    class Meta:
        db_table='order'
    
class payment(models.Model):
    customerid=models.ForeignKey(customer,on_delete=models.CASCADE)
    oid=models.ForeignKey(order,on_delete=models.CASCADE)
    paymentstatus=models.CharField(max_length=200,default="pending")
    transcationid=models.CharField(max_length=200)
    paymentmode=models.CharField(max_length=100,default="paypal")

    class Meta:
        db_table="payment"

class orderdetail(models.Model):
    ordernumber=models.CharField(max_length=100)
    customerid=models.ForeignKey(customer,on_delete=models.CASCADE)
    productid=models.ForeignKey(pet,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalprice=models.IntegerField()
    paymentid=models.ForeignKey(payment,on_delete=models.CASCADE,null=True)
    created_at=models.DateField(auto_now=True)
    updated_at=models.DateField(auto_now=True)

    class Meta:
        db_table='orderdetail'



    


