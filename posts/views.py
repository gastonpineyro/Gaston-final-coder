from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.select_related("autor")
        self.query = self.request.GET.get("q", "").strip()
        if self.query:
            queryset = queryset.filter(
                Q(titulo__icontains=self.query) | Q(contenido__icontains=self.query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.query
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, "Post publicado correctamente.")
        return super().form_valid(form)


class AutorRequeridoMixin(UserPassesTestMixin):
    """Solo el autor del post puede editarlo o eliminarlo."""

    def test_func(self):
        return self.get_object().autor == self.request.user


class PostUpdateView(LoginRequiredMixin, AutorRequeridoMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Post actualizado correctamente.")
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, AutorRequeridoMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        messages.success(self.request, "Post eliminado.")
        return super().form_valid(form)


class AboutView(TemplateView):
    template_name = "posts/about.html"
