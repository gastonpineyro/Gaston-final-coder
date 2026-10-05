import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Post

GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01"
    b"\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)
MEDIA_TEMPORAL = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class PostTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.autor = User.objects.create_user("autor", password="clave-segura-123")
        self.otro = User.objects.create_user("otro", password="clave-segura-123")
        self.post = Post.objects.create(
            titulo="Primer post", contenido="Contenido de Django", autor=self.autor
        )

    def test_lista_y_detalle_sin_imagen(self):
        self.assertContains(self.client.get(reverse("post_list")), "Primer post")
        respuesta = self.client.get(reverse("post_detail", args=[self.post.pk]))
        self.assertContains(respuesta, "Contenido de Django")

    def test_anonimo_redirige_al_login(self):
        urls = [
            reverse("post_create"),
            reverse("post_update", args=[self.post.pk]),
            reverse("post_delete", args=[self.post.pk]),
        ]
        for url in urls:
            respuesta = self.client.get(url)
            self.assertRedirects(respuesta, f"{reverse('login')}?next={url}")

    def test_crear_post_con_imagen(self):
        self.client.login(username="autor", password="clave-segura-123")
        imagen = SimpleUploadedFile("foto.gif", GIF, content_type="image/gif")
        respuesta = self.client.post(
            reverse("post_create"),
            {"titulo": "Con foto", "contenido": "Texto", "imagen": imagen},
        )
        nuevo = Post.objects.get(titulo="Con foto")
        self.assertRedirects(respuesta, nuevo.get_absolute_url())
        self.assertTrue(nuevo.imagen)
        self.assertContains(self.client.get(nuevo.get_absolute_url()), nuevo.imagen.url)

    def test_editar_y_eliminar_por_autor(self):
        self.client.login(username="autor", password="clave-segura-123")
        self.client.post(
            reverse("post_update", args=[self.post.pk]),
            {"titulo": "Editado", "contenido": "Nuevo texto"},
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.titulo, "Editado")
        self.client.post(reverse("post_delete", args=[self.post.pk]))
        self.assertFalse(Post.objects.exists())

    def test_otro_usuario_no_puede_editar_ni_eliminar(self):
        self.client.login(username="otro", password="clave-segura-123")
        self.assertEqual(
            self.client.get(reverse("post_update", args=[self.post.pk])).status_code, 403
        )
        self.assertEqual(
            self.client.post(reverse("post_delete", args=[self.post.pk])).status_code, 403
        )
        self.assertTrue(Post.objects.exists())

    def test_busqueda(self):
        url = reverse("post_list")
        self.assertContains(self.client.get(url, {"q": "django"}), "Primer post")
        self.assertContains(self.client.get(url, {"q": "inexistente"}), "No se encontraron posts")
