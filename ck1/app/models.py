from django.db import models 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import datetime

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    locality = models.CharField(max_length=150, verbose_name="Nearest Location")
    city = models.CharField(max_length=150, verbose_name="City")
    state = models.CharField(max_length=150, verbose_name="State")
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.locality
    


class  Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        ordering=('-name',)

    def __str__ (self):
        return self.name

class Sub_Category(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
   
    def __str__ (self):
        return self.name

class Products(models.Model):
    Availability = (('Item is available','Item is available'),('Item is not available','Item is not available'))

    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    sub_category = models.ForeignKey(Sub_Category,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cloud/pimg')
    price = models.IntegerField()
    Availability = models.CharField(choices=Availability,null=True,max_length=100)
    date = models.DateField(auto_now_add=True)   
    detail_description = models.TextField(blank=True, null=True, verbose_name="Detail Description")
    def __str__ (self):
        return self.name    
    

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True,label='Email',error_messages={'exists': 'This Already Exists'})

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'    

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    #def clean_email(self):
     #   if User.objects.filter(email=self.cleaned_data['email']).exists():
      #      raise forms.ValidationError(self.fields['email'].error_message['exists'])
       # return self.cleaned_data['email']     

class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self) -> str:
        return self.email



class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product= models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

    def prod_total(self):
        return (self.product.price * self.quantity)


STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)

class Order(models.Model):
    image = models.ImageField(upload_to='cloud/orderimg/imges')
    product = models.CharField(max_length=100,default='')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100,null=True)
    lastname = models.CharField(max_length=100,null=True)
    quantity = models.CharField(max_length=5)
    price = models.IntegerField()
    address = models.TextField()
    city = models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True )
    country = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=10)
    pincode = models.IntegerField()
    amount = models.CharField(max_length=100,null=True)
    total = models.CharField(max_length=100,null=True)
    date = models.DateField(default=datetime.datetime.today)    
    payment_id = models.CharField(max_length=300,null=True,blank=True)
    paid = models.BooleanField(default=False,null=True) 
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
        )

    def __str__(self):
        return self.product
    
class wishItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product= models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=5)

    def _str_(self):
        return self.product.name

    def prod_total(self):
        return (self.product.price * self.quantity)

class Restaurant(models.Model): 
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.CharField(max_length=100)
    address = models.TextField()    
    image = models.ImageField(upload_to='cloud/rimg',null=True) 

    def __str__(self) :
        return self.name 


class Coupon_Code(models.Model):
    code = models.CharField(max_length=100)
    discount = models.IntegerField()

    def __str__(self):
        return self.code
    
class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    product= models.ForeignKey(Products,on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    subject = models.CharField(max_length=100,blank=True)
    ip = models.CharField(max_length=20, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.subject
