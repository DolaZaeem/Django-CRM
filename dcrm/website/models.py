from django.db import models


# Create your models here.

class Quote_ovr(models.Model):
    id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    record_created_at = models.DateTimeField(auto_now_add=True)
    Quote_no = models.CharField(max_length = 50)
    Quote_date = models.DateField()
    Customer_name = models.CharField(max_length = 100)
    Customer_email = models.EmailField()
    Phone = models.CharField(max_length = 15)
    Address = models.CharField(max_length = 100)
    City = models.CharField(max_length = 50)
    State = models.CharField(max_length = 50)
    Zipcode = models.CharField(max_length = 20)

    #choices for currency
    CURRENCY= (('EUR','EURO'),
               ('USD','US DOLLAR'),
               ('GBP','GREAT BRITISH POUND'))

    Currency = models.CharField(max_length = 3, choices = CURRENCY,default ='EUR')

    def __str__(self):
        return(f"{self.Customer_name}")
    
class Quote_det(models.Model):
    record_created_at = models.DateTimeField(auto_now_add=True)
    Quote_no = models.ForeignKey(Quote_ovr,null=True,blank=True,on_delete =models.CASCADE)
    #Quote_no = models.CharField(max_length = 50) # Foreign Key
    Item_name = models.CharField(max_length = 200)
    Item_qty = models.PositiveIntegerField()
    Item_no = models.CharField(max_length = 50)

    def __str__(self):
        return(f"{self.Item_name}")