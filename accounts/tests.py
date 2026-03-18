from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.conf import settings

class LoginViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="TestPass123!",
        )

    def test_login_page_is_accessible(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_with_valid_credentials_redirects_to_schedule_index(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "testuser",
                "password": "TestPass123!",
            },
        )

        self.assertRedirects(response, reverse("schedule:index"))
    
    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            reverse(settings.LOGIN_URL),
            {
                "username": "testuser",
                "password": "TestPas123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

        error_message = "Por favor, introduzca un nombre de usuario y clave correctos. Observe que ambos campos pueden ser sensibles a mayúsculas."
        form = response.context["form"]
        # https://docs.djangoproject.com/en/6.0/topics/testing/tools/#django.test.SimpleTestCase.assertFormError
        self.assertFormError(form, None, error_message)

    def test_schedule_requires_authentication(self):
        response = self.client.get(reverse("schedule:index"))

        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('schedule:index')}",
        )

    def test_authenticated_user_is_redirected_away_from_login(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("accounts:login"))

        self.assertRedirects(response, reverse("schedule:index"))

class RegisterViewTests(TestCase):
    def test_register_page_is_accessible(self):
        response = self.client.get(reverse("accounts:register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")


    def test_create_user(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "testuser",
                "password1": "TestPass123!",
                "password2": "TestPass123!",
            },
        )

        self.assertRedirects(response, reverse(settings.LOGIN_URL))
        
        User = get_user_model()
        self.assertTrue(User.objects.filter(username="testuser").exists())
     

    def test_register_invalid(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "",  # inválido
                "password1": "123",
                "password2": "456",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

        error_message = "Hubo un error en el registro. Revisa los datos."
        form = response.context["form"]
        self.assertFormError(form, None, error_message)