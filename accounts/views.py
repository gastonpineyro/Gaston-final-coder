from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PerfilForm, RegistroForm, UsuarioForm
from .models import Perfil


def registro(request):
    if request.user.is_authenticated:
        return redirect("post_list")
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f"¡Bienvenido/a, {usuario.username}!")
            return redirect("post_list")
    else:
        form = RegistroForm()
    return render(request, "accounts/registro.html", {"form": form})


@login_required
def perfil(request):
    perfil_usuario, _ = Perfil.objects.get_or_create(usuario=request.user)
    return render(
        request,
        "accounts/perfil.html",
        {"perfil": perfil_usuario, "posts": request.user.posts.all()},
    )


@login_required
def editar_perfil(request):
    perfil_usuario, _ = Perfil.objects.get_or_create(usuario=request.user)
    if request.method == "POST":
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil_usuario)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, "Perfil actualizado.")
            return redirect("perfil")
    else:
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil_usuario)
    return render(
        request,
        "accounts/editar_perfil.html",
        {"usuario_form": usuario_form, "perfil_form": perfil_form},
    )
