from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def tiene_rol(user, *roles):
    """True si el usuario pertenece a alguno de los grupos indicados,
    o si es superusuario (el superusuario siempre puede todo)."""
    return user.groups.filter(name__in=roles).exists() or user.is_superuser


def requiere_rol(*roles):
    """
    Decorador para vistas: exige sesión iniciada (login_required) y
    además que el usuario esté en uno de los roles indicados.

    Uso:
        @requiere_rol("admin")
        def eliminar(request, pk): ...
    """
    def decorador(view_func):
        @wraps(view_func)
        @login_required(login_url="login")
        def wrapper(request, *args, **kwargs):
            if tiene_rol(request.user, *roles):
                return view_func(request, *args, **kwargs)
            messages.error(request, "No tienes permiso para esta acción.")
            return redirect("lista")
        return wrapper
    return decorador
