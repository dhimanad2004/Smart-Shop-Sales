from django.db import models

# Create your models here.
class SmartShopSales(models.Model):
    Item_Identifier=models.CharField(max_length=100)
    Item_Weight=models.CharField(max_length=100)
    Item_Fat_Content=models.CharField(max_length=100)
    Item_Visibility=models.CharField(max_length=100)
    Item_Type=models.CharField(max_length=100)
    Item_MRP=models.CharField(max_length=100)
    Outlet_Identifier=models.CharField(max_length=100)
    Outlet_Establishment_Year=models.CharField(max_length=100)
    Outlet_Size=models.CharField(max_length=100)
    Outlet_Location_Type=models.CharField(max_length=100)
    Outlet_Type=models.CharField(max_length=100)
    Item_Outlet_Sales=models.CharField(max_length=100)

class history(models.Model):
    Item_Weight=models.CharField(max_length=100)
    Item_Fat_Content=models.CharField(max_length=100)
    Item_Visibility=models.CharField(max_length=100)
    Item_Type=models.CharField(max_length=100)
    Item_MRP=models.CharField(max_length=100)
    Outlet_Size=models.CharField(max_length=100)
    Outlet_Location_Type=models.CharField(max_length=100)
    Outlet_Type=models.CharField(max_length=100)
    Item_Outlet_Sales=models.CharField(max_length=100,null=True)
