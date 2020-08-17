from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):

    #URLマッピングが正確にできているのか
    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    #正確なhtmlが返せているのかどうか
    # def test_home_page_returns_current_html(self):
        # request = HttpRequest()
        # response = home_page(request)
        # html = response.content.decode('utf8')
        # self.assertTrue(html.startswith('<html>'))
        # self.assertIn('<title>To-Do lists</title>', html)
        # self.assertTrue(html.endswith('</html>'))



        # response = self.client.get('/')
        # html = response.content.decode('utf8')
        # self.assertTrue(html.startswith('<html>'))
        # self.assertIn('<title>To-Do lists</title>', html)
        # self.assertTrue(html.strip().endswith('</html>'))
        # #正しいテンプレートが返ってきているか
        # self.assertTemplateUsed(response, 'lists/home.html')


    #TemplateUsedを使ってurlの解決
    def test_users_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')


    # POSTリクエスト
    def test_can_save_a_POST_requset(self):
        self.client.post('/', data={'item_text': 'A new list item'})
        # 追加されたかどうか
        self.assertEqual(Item.objects.count(), 1)
        # 正しく取り出せているかどうか
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")


    # GETリクエスト
    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        # POSTの後にリダイレクトされてい るか
        self.assertEqual(response.status_code, 302)
        # リダイレクト先が正しいかどうか
        self.assertEqual(response['location'], '/')

    
    def test_displays_all_lits_items(self):
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


    
class ItemModelTest(TestCase):

    def test_saving_and_retrieving_item(self):
        first_item = Item()
        first_item.text = 'The first(ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first(ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')






