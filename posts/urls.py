from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("posts/nuevo/", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/editar/", views.PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/eliminar/", views.PostDeleteView.as_view(), name="post_delete"),
    path("acerca/", views.AboutView.as_view(), name="about"),
]
