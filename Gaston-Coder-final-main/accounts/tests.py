from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class CuentasTests(TestCase):
    def test_registro_crea_usuario_perfil_e_inicia_sesion(self):
        respuesta = self.client.post(
            reverse("registro"),
            {
                "username": "nuevo",
                "email": "nuevo@example.com",
                "password1": "clave-segura-123",
                "password2": "clave-segura-123",
            },
        )
        self.assertRedirects(respuesta, reverse("post_list"))
        usuario = User.objects.get(username="nuevo")
        self.assertTrue(hasattr(usuario, "perfil"))
        self.assertContains(self.client.get(reverse("post_list")), "Cerrar sesión")

    def test_login_y_logout(self):
        User.objects.create_user("ana", password="clave-segura-123")
        respuesta = self.client.post(
            reverse("login"), {"username": "ana", "password": "clave-segura-123"}
        )
        self.assertRedirects(respuesta, reverse("post_list"))
        self.client.post(reverse("logout"))
        self.assertContains(self.client.get(reverse("post_list")), "Iniciar sesión")

    def test_perfil_protegido(self):
        for nombre in ["perfil", "editar_perfil"]:
            url = reverse(nombre)
            self.assertRedirects(self.client.get(url), f"{reverse('login')}?next={url}")

    def test_editar_perfil(self):
        User.objects.create_user("ana", password="clave-segura-123")
        self.client.login(username="ana", password="clave-segura-123")
        self.client.post(
            reverse("editar_perfil"),
            {"first_name": "Ana", "last_name": "López", "email": "ana@example.com", "biografia": "Hola"},
        )
        self.assertContains(self.client.get(reverse("perfil")), "Ana López")
