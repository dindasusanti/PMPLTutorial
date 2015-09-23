from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item, List

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/lists/the-only-list-in-the-world/')
	
	comment = 'yey, waktunya berlibur'	

	items = Item.objects.all()		
	return render(request, 'home.html', {'comment':comment})
	
def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	
	if Item.objects.filter(list_id=list_.id).count()==0:
		comment = 'yey, waktunya berlibur'
	elif Item.objects.filter(list_id=list_.id).count()<5:
		comment = 'sibuk tapi santai'
	else:
		comment = 'oh tidak'
	
	return render(request, 'list.html', {'list': list_, 'comment':comment})
	#items = Item.objects.filter(list=list_)
	#items = Item.objects.all()
	#return render(request, 'list.html', {'items': items})

def new_list(request):
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
	list_ = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' % (list_.id,))
