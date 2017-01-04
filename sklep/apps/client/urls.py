from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^search/$', search_items, name='search'),
    url(r'^order/$', make_order, name='order'),
    url(r'^product-details/(\d+)$', product_detail, name='detail'),
]
