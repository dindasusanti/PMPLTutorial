from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List

class ListAndItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()
		
		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)		

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

	#def test_home_page_display_to_do_list_empty(self):
		#request = HttpRequest()
		#response = home_page(request)
		
		#self.assertEqual(Item.objects.count(), 0)
		#self.assertIn('yey, waktunya berlibur', response.content.decode())

	#def test_home_page_display_to_do_list_less_5(self):
		#Item.objects.create(text='Item 1')
		
		#request = HttpRequest()
		#response = home_page(request)

		#self.assertLess(Item.objects.count(), 5)
		#self.assertIn('sibuk tapi santai', response.content.decode())

	#def test_home_page_display_to_do_list_greater_equal_5(self):
		#Item.objects.create(text='Item 1')
		#Item.objects.create(text='Item 2')
		#Item.objects.create(text='Item 3')
		#Item.objects.create(text='Item 4')
		#Item.objects.create(text='Item 5')

		#request = HttpRequest()
		#response = home_page(request)

		#self.assertGreaterEqual(Item.objects.count(), 5)
		#self.assertIn('oh tidak', response.content.decode())

class ListViewTest(TestCase):
	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_all_items(self):
		list_ = List.objects.create()
		Item.objects.create(text='itemey 1', list=list_)
		Item.objects.create(text='itemey 2', list=list_)

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

		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
		#self.assertEqual(response.status_code, 302)
		#self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
		
