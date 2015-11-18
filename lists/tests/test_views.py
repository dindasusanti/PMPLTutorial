from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page, view_list
from lists.models import Item, List

class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html', {'comment':'yey, waktunya berlibur'})
		#self.assertTrue(response.content.startswith(b'<html>'))
		#self.assertIn(b'<title>To-Do</title>',response.content)
		#self.assertTrue(response.content.strip().endswith(b'</html>'))
		self.assertEqual(response.content.decode(), expected_html)

	#def test_home_page_can_save_a_POST_request(self):
		#request = HttpRequest()
		#request.method = 'POST'
		#request.POST['item_text']='A new list item'

		#response = home_page(request)
		
		#self.assertEqual(Item.objects.count(), 1)
		#new_item = Item.objects.first()
		#self.assertEqual(new_item.text, 'A new list item')		

		#self.assertIn('A new list item', response.content.decode())
		#expected_html = render_to_string('home.html',{'new_item_text': 'A new list item'})
		#self.assertEqual(response.content.decode(), expected_html)
		
	#def test_home_page_redirects_after_POST(self):
		#request = HttpRequest()
		#request.method = 'POST'
		#request.POST['item_text'] = 'A new list item'

		#response = home_page(request)
		
		#self.assertEqual(response.status_code, 302)
		#self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
	def test_home_page_only_saves_items_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.count(), 0)

	#def test_home_page_displays_all_list_items(self):
		#Item.objects.create(text='itemey 1')
		#Item.objects.create(text='itemey 2')

		#request = HttpRequest()
		#response = home_page(request)

		#self.assertIn('itemey 1', response.content.decode())
		#self.assertIn('itemey 2', response.content.decode())

	def test_home_page_display_to_do_list_empty(self):
		request = HttpRequest()
		response = home_page(request)
		
		self.assertEqual(Item.objects.count(), 0)
		self.assertIn('yey, waktunya berlibur', response.content.decode())

	def test_home_page_display_to_do_list_less_5(self):
		list_ = List.objects.create()
		Item.objects.create(text='itemey 1', list=list_)		

		request = HttpRequest()
		response = view_list(request, list_.id)

		self.assertLess(Item.objects.filter(list_id=list_.id).count(), 5)
		self.assertIn('sibuk tapi santai', response.content.decode())

	def test_home_page_display_to_do_list_greater_equal_5(self):
		list_ = List.objects.create()
		Item.objects.create(text='Item 1', list=list_)
		Item.objects.create(text='Item 2', list=list_)
		Item.objects.create(text='Item 3', list=list_)
		Item.objects.create(text='Item 4', list=list_)
		Item.objects.create(text='Item 5', list=list_)		

		#Item.objects.create(text='Item 1')
		#Item.objects.create(text='Item 2')
		#Item.objects.create(text='Item 3')
		#Item.objects.create(text='Item 4')
		#Item.objects.create(text='Item 5')

		request = HttpRequest()
		response = view_list(request, list_.id)

		self.assertGreaterEqual(Item.objects.filter(list_id=list_.id).count(), 5)
		self.assertIn('oh tidak', response.content.decode())

class ListViewTest(TestCase):
	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_all_items(self):
		list_ = List.objects.create()
		Item.objects.create(text='itemey 1', list=list_)
		Item.objects.create(text='itemey 2', list=list_)
	
	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)

		response = self.client.get('/lists/%d/'% (correct_list.id,))
		
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/lists/%d/' % (correct_list.id,))
		self.assertEqual(response.context['list'], correct_list)
		#response = self.client.get('/lists/the-only-list-in-the-world/')
		
		#self.assertContains(response, 'itemey 1')
		#self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):
	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		
		new_list = List.objects.first()
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
		#self.assertEqual(response.status_code, 302)
		#self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

class NewItemTest(TestCase):
	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			'/lists/%d/add_item' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertEqual(Item.objects.count(),1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			'/lists/%d/add_item' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))	
