from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=250, blank=True)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to="posts/", blank=True, null=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.pk])
