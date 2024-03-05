from django.db import models


# Create your models here.


class Quote_ovr(models.Model):
    record_created_at = models.DateTimeField(auto_now_add=True)
    Quote_no = models.CharField(max_length = 50,unique=True,null=False)
    Quote_date = models.DateField(null=True)
    Customer_name = models.CharField(max_length = 100,null=True)
    Customer_email = models.EmailField(null=True)
    Phone = models.CharField(max_length = 15,null=True)
    Address = models.CharField(max_length = 100,null=True)
    City = models.CharField(max_length = 50,null=True)
    State = models.CharField(max_length = 50,null=True)
    Zipcode = models.CharField(max_length = 20,null=True)
    #choices for currency
    CURRENCY= (('EUR','EURO'),
               ('USD','US DOLLAR'),
               ('GBP','GREAT BRITISH POUND'))

    Currency = models.CharField(max_length = 3, choices = CURRENCY)
    def __str__(self):
        return(f"{self.Quote_no}-{self.Customer_name}")
    
class Quote_det(models.Model):
    record_created_at = models.DateTimeField(auto_now_add=True)
    Quote_no = models.ForeignKey(Quote_ovr,null=True,blank=True,on_delete =models.CASCADE)
    Item_name = models.CharField(max_length = 200,null=True)
    Item_qty = models.PositiveIntegerField(null=True)
    Item_no = models.CharField(max_length = 50,null=True)

    def __str__(self):
        return(f"{self.Item_name}")