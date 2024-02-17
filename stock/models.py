from django.db import models

# Create your models here.
class Data(models.Model):
    stock_name = models.CharField(max_length=200, unique=True)
    open_date = models.DateField()
    close_date = models.DateField()
    fixed_price = models.IntegerField()
    min_hprice = models.IntegerField()
    max_hprice = models.IntegerField()
    trading_firm = models.TextField()
    crawled_datetime = models.DateTimeField(auto_now=True)

class FirmData(models.Model):
    firm_name = models.TextField()
    firm_link = models.TextField()