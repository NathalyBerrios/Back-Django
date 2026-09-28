from rest_framework import permissions

from .decorators import tiene_rol


class PermisoPorRol(permissions.BasePermission):

    def has_permission(self, request, view):
        usuario = request.user

        # 1. Sin autenticar, nadie pasa.
        if not (usuario and usuario.is_authenticated):
            return False

        # 2. Leer (GET, HEAD, OPTIONS): cualquier usuario autenticado.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 3. Crear (POST): admin o normal.
        if request.method == "POST":
            return tiene_rol(usuario, "admin", "normal")

        # 4. Editar (PUT, PATCH) y borrar (DELETE): solo admin.
        return tiene_rol(usuario, "admin")
