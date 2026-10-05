from django import forms

from blog_config.form_mixins import BootstrapFormMixin

from .models import Post


class PostForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "subtitulo", "contenido", "imagen"]
        widgets = {
            "contenido": forms.Textarea(attrs={"rows": 10}),
        }
        labels = {
            "titulo": "Título",
            "subtitulo": "Subtítulo",
            "contenido": "Contenido",
            "imagen": "Imagen",
        }
