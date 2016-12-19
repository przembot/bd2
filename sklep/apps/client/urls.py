from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^search/$', search_items, name='search'),
    url(r'^order/$', make_order, name='order'),
    url(r'^product-details/$', product_detail, name='detail'),
]
