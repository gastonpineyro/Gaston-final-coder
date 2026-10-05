# Blog Web — Proyecto Final

Blog web hecho con Django. Cualquier visitante puede leer y buscar publicaciones. Los usuarios registrados pueden crear, editar y eliminar sus propios posts con imagen, y tienen un perfil con avatar y biografía.

## Tecnologías utilizadas

- Python 3.10+
- Django 5.2
- Pillow (manejo de imágenes)
- python-decouple (variables de entorno)
- SQLite (base de datos de desarrollo)
- Bootstrap 5 (estilos, cargado por CDN)
- HTML / CSS

## Funcionalidades principales

- **CRUD de posts** desde la interfaz web: listar, ver detalle, crear, editar y eliminar.
- **Imágenes en los posts**: se cargan desde el formulario y se muestran en el listado y el detalle. Si un post no tiene imagen, el template muestra un recuadro "Sin imagen" y no se rompe.
- **Usuarios**: registro, login y logout.
- **Perfil**: muestra los datos del usuario y sus posts. Se puede editar nombre, apellido, email, biografía e imagen de perfil.
- **Anónimo vs. autenticado**: la barra de navegación cambia según haya sesión iniciada o no.
- **Rutas protegidas**: crear, editar y eliminar posts, y ver y editar el perfil requieren sesión iniciada. La protección está en las vistas (`LoginRequiredMixin` y `@login_required`): si un visitante anónimo entra a esas URLs, se lo redirige al login.
- **Permisos de autor**: solo el autor de un post puede editarlo o eliminarlo (otro usuario recibe un error 403).
- **Búsqueda** por título o contenido, con aviso cuando no hay coincidencias.
- Paginación del listado y mensajes de confirmación.

## Estructura del proyecto

```
├── blog_config/     # Configuración del proyecto (settings, urls)
├── posts/           # App de publicaciones (modelo Post, CRUD, búsqueda)
├── accounts/        # App de usuarios (registro, login, perfil)
├── templates/       # Templates HTML
├── static/css/      # Estilos propios
├── manage.py
├── requirements.txt
└── .env.example
```

## Instalación y ejecución local

1. Cloná el repositorio y entrá a la carpeta:
   ```bash
   git clone https://github.com/gastonpineyro/Gaston-final-coder.git
   cd Gaston-final-coder
   ```

2. Creá y activá un entorno virtual:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. Instalá las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Creá el archivo `.env` a partir del ejemplo (**obligatorio**: sin este archivo el proyecto no arranca):
   ```bash
   # Windows
   copy .env.example .env
   # macOS / Linux
   cp .env.example .env
   ```
   Abrí `.env` y reemplazá `SECRET_KEY` por una clave propia. Podés generar una con:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. Aplicá las migraciones:
   ```bash
   python manage.py migrate
   ```

6. (Opcional) Creá un superusuario para entrar al panel de administración en `/admin/`:
   ```bash
   python manage.py createsuperuser
   ```

7. Iniciá el servidor:
   ```bash
   python manage.py runserver
   ```

8. Abrí http://127.0.0.1:8000/ en el navegador.

### Probar desde cero

El repositorio **no incluye** `db.sqlite3` ni la carpeta `media/` (están en `.gitignore`). Después de `migrate` la base queda vacía:

1. Entrá a **Registrarse** y creá un usuario (quedás logueado automáticamente).
2. Usá **Nuevo post** para crear publicaciones, con y sin imagen.
3. La carpeta `media/` se crea sola al subir la primera imagen.
4. Cerrá sesión y probá entrar a `/posts/nuevo/` o `/accounts/perfil/`: te tiene que redirigir al login.

### Tests

El proyecto incluye tests automáticos del CRUD, las imágenes, la búsqueda, el registro, el login/logout y las rutas protegidas:
```bash
python manage.py test
```

## Rutas principales

| URL | Descripción | Requiere sesión |
|---|---|---|
| `/` | Listado de posts y búsqueda (`?q=`) | No |
| `/posts/<id>/` | Detalle de un post | No |
| `/posts/nuevo/` | Crear post | Sí |
| `/posts/<id>/editar/` | Editar post (solo autor) | Sí |
| `/posts/<id>/eliminar/` | Eliminar post (solo autor) | Sí |
| `/acerca/` | Acerca del blog | No |
| `/accounts/registro/` | Registro | No |
| `/accounts/login/` | Login | No |
| `/accounts/perfil/` | Ver perfil | Sí |
| `/accounts/perfil/editar/` | Editar perfil | Sí |
| `/admin/` | Panel de administración | Superusuario |

## Autor

**Gaston Pineyro** — [github.com/gastonpineyro](https://github.com/gastonpineyro)

Entrega final del curso de Python — CoderHouse.
