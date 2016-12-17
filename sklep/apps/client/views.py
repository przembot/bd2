from django.shortcuts import render
from apps.dao.models import *
from apps.accounts.models import Client
import json
from datetime import datetime
from django.db import transaction
from django.http import HttpResponse

def index(request):
	return render(request, 'index.html')

def get_categories(request):
	cats = Category.objects.all()
	return cats

def db_search_items(cat_id=None, name=None):
	"""
	Odwolaj sie do bd i pobierz wszystkie itemy z danej kategori i/lub majace w nazwie name
	Jesli oba parametry sa None - zwraca wszystkie itemy
	@return: lista Item
	"""
	items = Item.objects.all()
	if cat_id is not None:
		if name is None:
			filtered_items = items.filter(category_id=cat_id)
		else:
			filtered_items = items.filter(category_id=cat_id, name__itcontains=name)
		return filtered_items

	return items

def search_items(request, cat_id=None, name=None):
	print(request.GET["cat_id"])
	print(request.GET["name"])
	return render(request, 'index.html')

def make_order(request):
	if request.method == 'POST':
		#json_data = json.loads(request.body) #for python2?
		order = json.loads(request.body.decode("utf-8"))
		price_dict = {}
		for itemspec in order['items']:
			item_id = itemspec['id']
			amount = itemspec['amount']
			try:
				item = Item.objects.get(id=item_id)
				price_dict[item_id] = item.price
				if item.in_stock < amount:
					return HttpResponseBadRequest()
			except Item.DoesNotExist:
				return HttpResponseBadRequest()


			with transaction.atomic():
				new_order = Order(status_change_date=datetime.now,
								payment_status=0,
								client_id=Client.objects.get(user=request.user))
				new_order.save()
				for itemspec in order['items']:
				# CHECK THIS: additional list of order_items may be required
				# if objects is created locally and destroyed in the same iteration
					order_item = Order_Item(quantity=itemspec['amount'],
											price=price_dict[itemspec['id']],
											order_id=new_order.id,
											item_id=itemspec['id'])
					order_item.save()

	return HttpResponse()
