from django.contrib import admin
from .models import Coupon

# Register your models here.
class CouponAdmin(admin.ModelAdmin):
    
    list_display = ["code", "company_name", "availability"]

admin.site.register(Coupon, CouponAdmin)
