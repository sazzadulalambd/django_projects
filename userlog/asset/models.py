from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Asset(models.Model):
    name = models.TextField(max_length= 20)
    image = models.ImageField(upload_to='images/')
    brand_name = models.TextField(max_length= 20)
    model = models.TextField(max_length= 20)
    sn_number = models.TextField(max_length= 200)
    description = models.TextField(max_length=500)
    purchase_date = models.DateField()
    expire_Date = models.DateField()
    price = models.TextField(max_length= 10)
    invoice_img = models.ImageField(upload_to='invoices/')  
    status = models.TextField(max_length= 10)          
    report = models.TextField(max_length= 500)
    def __str__(self):
        return self.sn_number


class AssetAssigningList(models.Model):
    employee_id = models.ForeignKey(User, on_delete= models.DO_NOTHING)
    asset_id = models.ForeignKey(Asset, on_delete= models.DO_NOTHING)
    purchase_date = models.DateField()
    expire_Date = models.DateField()
    status = models.TextField(max_length= 10)          


class AssetReportList(models.Model): 
    employee_id = models.ForeignKey(User, on_delete= models.DO_NOTHING)
    asset_id = models.ForeignKey(Asset, on_delete= models.DO_NOTHING)
    date = models.DateField()
    issue = models.TextField(max_length= 20)
    description = models.TextField(max_length= 200)
    status = models.TextField(max_length= 10)          
    message = models.TextField(max_length= 20)


# class UploadImage(models.Model):  
#     caption = models.CharField(max_length=200)  
#     image = models.ImageField(upload_to='images')  
  
#     def __str__(self):  
#         return self.caption  