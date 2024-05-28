"""Coupon management urls"""

from django.urls import path
from .views import *

urlpatterns = [
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('admin/coupons/', CouponCreateView.as_view(), name='create_list_coupons'),
    path('coupons/search/', CouponSearchView.as_view(), name='search_coupons'),
    path('coupons/avail/', CouponAvailView.as_view(), name='avail_coupon'),
]