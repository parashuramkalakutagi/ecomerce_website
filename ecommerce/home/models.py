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
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0,null=True,blank=True)
    catagory = models.CharField(choices=CATAGORY_CHOICES,max_length=5)
    lable = models.CharField(choices=LABALE_CHOICES,max_length=5)
    discount_price = models.FloatField(null=True,blank=True)
    description = models.TextField(null=True,blank=True,default=False)


    def __str__(self):
        return self.title

class orderitem(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ForeignKey(item,on_delete=models.CASCADE,related_name='orderitem',related_query_name='orderitem')
    quntity = models.IntegerField(default=1)

    def __str__(self):
        return self.item
class order(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(orderitem,related_name='order',related_query_name='order')
    created_at = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user