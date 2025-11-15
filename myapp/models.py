from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Brand(models.Model):
    brandname = models.CharField(max_length=100, null=True, blank=True)
    brandlogo = models.FileField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.brandname

class Technician(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    technicianname = models.CharField(max_length=100, null=True, blank=True)
    technicianid = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobileno = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    pic = models.FileField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    #
    # def __str__(self):
    #     return self.policename

class About(models.Model):
   pagetitle = models.CharField(max_length=100, null=True, blank=True)
   description = models.CharField(max_length=100, null=True, blank=True)

class Contact(models.Model):
    pagetitle = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    contactno = models.CharField(max_length=100, null=True, blank=True)

class Register(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

class Request(models.Model):
    register = models.ForeignKey(Register, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE, null=True, blank=True)
    actype = models.CharField(max_length=100, null=True, blank=True)
    accapacity = models.CharField(max_length=100, null=True, blank=True)
    natureofproblem = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    servicenumber = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    dateofservice = models.CharField(max_length=100, null=True, blank=True)
    suitabletime = models.CharField(max_length=100, null=True, blank=True)
    totalprice = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, default="Not Updated Yet", null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.actype

class Trackinghistory(models.Model):
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    remark1 = models.CharField(max_length=100, null=True, blank=True)
    remark2 = models.CharField(max_length=100, null=True, blank=True)
    servicecharge = models.CharField(max_length=100, null=True, blank=True)
    partcharge = models.CharField(max_length=100, null=True, blank=True)
    othercharge = models.CharField(max_length=100, null=True, blank=True)
    status1 = models.CharField(max_length=100, null=True, blank=True)
    status2 = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, default="Not Updated Yet", null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

class Cancel(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True, blank=True)
    reasonforcancel = models.CharField(max_length=100, null=True, blank=True)




