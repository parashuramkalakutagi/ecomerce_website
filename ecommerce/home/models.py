from django.db import models
from accounts.models import User
import uuid

class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract  = True

CATAGORY_CHOICES = (
    ('s','shirt'),
    ('sport','sports wear'),
    ('ow','out wear')
)

LABALE_CHOICES = (
    ('p','primary'),
    ('s','secondry'),
    ('d','danger')
)



class item(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='product_images',null=True)
    title = models.CharField(max_length=100)
    price = models.IntegerField(default=0,null=True,blank=True)
    catagory = models.CharField(choices=CATAGORY_CHOICES,max_length=5)
    lable = models.CharField(choices=LABALE_CHOICES,max_length=5)
    discount_price = models.FloatField(null=True,blank=True)
    description = models.TextField(null=True,blank=True,default=False)
    currency = models.CharField(max_length=100,default='INR')



    def __str__(self):
        return self.title

class orderitem(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ForeignKey(item,on_delete=models.CASCADE,related_name='orderitem',related_query_name='orderitem')
    quntity = models.IntegerField(default=1)




class order(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ForeignKey(orderitem,on_delete=models.CASCADE,related_name='order',related_query_name='order')
    created_at = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    amount = models.IntegerField(default=0,null=True,blank=True)
    currency = models.CharField(max_length=100,default='INR')





class Amount_transaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255)
    order_id = models.CharField(max_length=300)
    signature = models.CharField(max_length=500)
    amount = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)