from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from http import HTTPStatus

class HomeGetRedirectTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.resp = self.client.get(r('home'))
        self.resp2 = self.client.get(r('home'),follow=True)

    def test_response(self):
        self.assertEqual(self.resp.status_code , HTTPStatus.FOUND)
        self.assertEqual(self.resp2.status_code , HTTPStatus.OK)
    
    def test_labels_html(self):
        tags = (
            ('<form', 1),
            ('</form>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp2, text, count)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'login.html')


class HomeGetTest(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(username='admin',email='aluno@fatec.sp.gov.br')
        new_user.set_password('123mudar')
        new_user.save()
        self.client.login(username="admin", password="123mudar")
        self.resp = self.client.get(r('home'))
        self.resp2 = self.client.get(r('home'),follow=True)

    def test_response(self):
        self.assertEqual(self.resp.status_code , HTTPStatus.OK)
        self.assertEqual(self.resp2.status_code , HTTPStatus.OK)
    
    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'index.html')

