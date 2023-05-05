from django.contrib import admin

# Register your models here.
from .models import Category,Sub_Category,Products,Contact_us,Cart,Order,Address,wishItem,Restaurant,Coupon_Code,Review
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Products)
admin.site.register(Contact_us)
admin.site.register(Order)
#admin.site.register(Cart)
admin.site.register(Address)
#admin.site.register(wishItem)
#admin.site.register(Restaurant)
#admin.site.register(Coupon_Code)
#admin.site.register(Review)





