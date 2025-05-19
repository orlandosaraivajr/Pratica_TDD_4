from django.test import TestCase
from django.contrib.auth import get_user_model
from core.forms import LoginForm

UserModel = get_user_model()

class LoginFormTest(TestCase):
    def setUp(self):
        self.valid_user = UserModel.objects.create_user(
            username='orlando',
            email='orlando@fatec.sp.gov.br',
            password='senha123'
        )

    def test_form_has_fields(self):
        form = LoginForm()
        expected = ['email', 'password']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_email_must_be_institucional(self):
        form = self.make_validated_form(email='usuario@gmail.com')
        self.assertIn('email', form.errors)
        self.assertIn('Informe seu e-mail institucional.', form.errors['email'])

    def test_email_field_required(self):
        form = self.make_validated_form(email='')
        self.assertIn('email', form.errors)

    def test_invalid_email_not_found(self):
        form = self.make_validated_form(email='naoexiste@fatec.sp.gov.br')
        self.assertIn('__all__', form.errors)
        self.assertIn('Usuário com esse e-mail não encontrado.', form.errors['__all__'])

    def test_wrong_password(self):
        form = self.make_validated_form(password='senhaerrada')
        self.assertIn('__all__', form.errors)
        self.assertIn('Senha incorreta para o e-mail informado.', form.errors['__all__'])

    def test_authenticates_user(self):
        form = self.make_validated_form()
        self.assertTrue(form.is_valid())
        self.assertEqual(form.user, self.valid_user)

    def make_validated_form(self, **kwargs):
        valid = dict(email='orlando@fatec.sp.gov.br', password='senha123')
        data = dict(valid, **kwargs)
        form = LoginForm(data=data)
        form.is_valid()
        return form