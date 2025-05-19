from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from http import HTTPStatus
from core.forms import LoginForm


class Login_OK_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(email='aluno.fatec@fatec.sp.gov.br',username='admin')
        new_user.set_password('123mudar')
        new_user.save()
        data = {'email':'aluno.fatec@fatec.sp.gov.br', 'password':'123mudar'}
        self.resp = self.client.post(r('login'), data)
        self.resp2 = self.client.post(r('login'), data, follow=True)
        
    def test_response(self):
        self.assertEqual(self.resp.status_code , HTTPStatus.FOUND)
        self.assertEqual(self.resp2.status_code , HTTPStatus.OK)
    
    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'index.html')


class Login_Fail_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(email='aluno.fatec@fatec.sp.gov.br',username='admin')
        new_user.set_password('SENHA_ERRADA')
        new_user.save()
        data = {'username':'admin', 'password':'123mudar'}
        self.resp = self.client.post(r('login'), data)
 
    def test_response(self):
        self.assertEqual(self.resp.status_code , HTTPStatus.OK)
    
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'login.html')


class Login_GET_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.resp = self.client.get(r('login'))
 
    def test_response(self):
        self.assertEqual(self.resp.status_code , HTTPStatus.OK)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'login.html')

    def test_context(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, LoginForm)


class Logout_Get_OK_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(email='aluno.fatec@fatec.sp.gov.br',username='admin')
        new_user.set_password('123mudar')
        new_user.save()
        self.client.login(username="admin", password="123mudar")
        self.resp = self.client.get(r('logout'), follow=True)

    def test_response(self):
        self.assertEqual(self.resp.status_code , HTTPStatus.OK)
    
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'index.html')


class Logout_Post_OK_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(email='aluno.fatec@fatec.sp.gov.br',username='admin')
        new_user.set_password('123mudar')
        new_user.save()
        self.client.login(username="admin", password="123mudar")
        self.resp = self.client.post(r('logout'))
        
    def test_response(self):
        self.assertEqual(self.resp.status_code , HTTPStatus.OK)
    
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'logout.html')