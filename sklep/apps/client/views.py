from django.shortcuts import render
from apps.dao.models import *
from apps.accounts.models import Client
import json
from datetime import datetime
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import sys, traceback
import os

def index(request):
    return render(request, 'my-orders.html')

def get_categories(request):
    cats = Category.objects.all()
    return cats

def get_orders(request):
    try:
        user = Client.objects.get(user=request.user)
        orderList = Order.objects.filter(client_id=user.id)
        orderDict = {}
        for order in orderList:
           orderList = Order_Item.objects.select_related().filter(order_id=order.id)
           orderDict[order] = orderList

        return render(request, template_name='my-orders.html',
                      context={'orderDict' : orderdict})

    except Client.DoesNotExist:
        return render(request.path)

def product_reviews(prod_id=None):
    """
    FIXME: This kind of copy-pasted from product-detail
    If this function is only used in product-detail
    I propose to remove it and just use line 36
    Mati
    """
    if prod_id is not None:
        try:
            reviewList = Review.objects.filter(id=prod_id)
            return reviewList

        except Review.DoesNotExist:
            pass

def product_detail(request, prod_id=None):
    if prod_id is not None:
        try:
            product = Item.objects.get(id=prod_id)
            reviewList = product_reviews(prod_id)
            return render(request, template_name='product-details.html',
                          context={'product' : product, 'reviews' : reviewList})

        except Item.DoesNotExist:
            return render(request.path)

def db_search_items(cat_id=None, name=None):
    """
    Odwolaj sie do bd i pobierz wszystkie itemy z danej kategori i/lub majace w nazwie name
    Jesli oba parametry sa None - zwraca wszystkie itemy
    @return: lista Item
    """
    items = Item.objects.all()

    # return all items
    if cat_id is None and name is None:
        filtered_items = items

    # search inside category
    elif cat_id is not None:
        if name is None:
            filtered_items = items.filter(category_id=cat_id)
        else:
            filtered_items = items.filter(category_id=cat_id, name__itcontains=name)

    # search items by name without specifying category
    else:
        filtered_items = items.filter(name__itcontains=name)

    return filtered_items

def search_items(request, cat_id=None, name=None):
    print(request.GET["cat_id"])
    print(request.GET["name"])
    return render(request, 'index.html')

@login_required
def make_order(request):
    if request.method == 'POST':
        #json_data = json.loads(request.body) #for python2?
        order = json.loads(request.body.decode("utf-8"))

        try:
            client = Client.objects.get(user=request.user)

            with transaction.atomic():
                new_order = Order.objects.create(status_change_date=timezone.now(),
                                                 payment_status=0,
                                                 client_id=client)
                """
                Possible hazard condition here
                if select_for_update() locks row for changing and locking
                which is true according to Django doc, then it is possible
                for other thread/process to get wrong count of items in stock
                and order too many items - Mati
                FIXME: Need to be analyzed
                """
                for itemspec in order['items']:
                    item_id = itemspec['id']
                    amount = itemspec['amount']

                    # select_for_update locks db row until the end of transaction
                    item = Item.objects.select_for_update().get(id=item_id)
                    if amount >= 1 and item.in_stock >= amount:
                        item.in_stock -= amount
                        item.save()
                        Order_Item.objects.create(quantity=amount,
                                                  price=item.price,
                                                  order_id=new_order,
                                                  item_id=item)
                    else:
                        raise Exception('Wrong ammount supplied for ' +
                                        'item with id: ' + str(item_id))

                if order['invoice'] is True:
                    # create invoice here
                    pass
        except Exception as e:
            # if exception is database exception,
            # Django will do full rollback automatically here
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno) +
                  os.linesep +
                  str(e))
            return HttpResponseBadRequest()

    return HttpResponse()
