from django.db import models
from django.forms import ValidationError


# Create your models here.

'''def validate_currency(value):
    if value not in Quote_ovr.CURRENCY:
        raise ValidationError('Invalid currency. Must be one of: ',Quote_ovr.CURRENCY)'''
    
class Quote_ovr(models.Model):
    record_created_at = models.DateTimeField(auto_now_add=True)
    Quote_no = models.CharField(max_length = 50,unique=True,null=False)
    Quote_date = models.DateField(null=True)
    Customer_name = models.CharField(max_length = 100,null=True)
    Customer_email = models.EmailField(null=True)
    Phone = models.CharField(max_length = 15,null=True)
    Country = models.CharField(max_length = 100,null=True)
    State = models.CharField(max_length = 50,null=True)
    City = models.CharField(max_length = 50,null=True)
    Zipcode = models.CharField(max_length = 20,null=True)

    #choices for currency
    CURRENCY= (('EUR','EURO'),
               ('USD','US DOLLAR'),
               ('GBP','GREAT BRITISH POUND'))
    #choices for Customer Type
    CustomerType= (('RET','Retailer'),
               ('WHO','Wholesaler')
               )

    Currency = models.CharField(max_length = 4, choices = CURRENCY)
    Customer_Type = models.CharField(max_length = 4, choices = CustomerType)

    def __str__(self):
        return(f"{self.Quote_no}")
    

        
class Quote_det(models.Model):
    record_created_at = models.DateTimeField(auto_now_add=True)
    Quote_ref = models.ForeignKey(Quote_ovr,null=False,blank=False,on_delete =models.CASCADE,to_field='Quote_no')
    Item_name = models.CharField(max_length = 200,null=True)
    Item_qty = models.PositiveIntegerField(null=True)
    Item_no = models.CharField(max_length = 50,null=True)
    Item_per_unit_price = models.PositiveIntegerField(null=True,default = 0)


    def __str__(self):
        return(f"{self.Item_name}")
    
    @property
    def product_line_total(self):
        return self.Item_qty * self.Item_per_unit_price