from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/')
	
	if Item.objects.count()==0:
		comment = 'yey, waktunya berlibur'
	elif Item.objects.count()<5:
		comment = 'sibuk tapi santai'
	else:
		comment = 'oh tidak'	

	items = Item.objects.all()		
	return render(request, 'home.html', {'items': items, 'comment':comment})
		#new_item_text = request.POST['item_text']
		#Item.objects.create(text=new_item_text)
	#else:
		#new_item_text = ''
		#return HttpResponse(request.POST['item_text'])
	#item = Item()
	#item.text = request.POST.get('item_text', '')
	#item.save()
	
	#return render(request, 'home.html', {'new_item_text': new_item_text,})
