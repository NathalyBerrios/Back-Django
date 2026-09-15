from decouple import config
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

from core.models import Registro

# 1. Los tres roles que pide la pauta
grupo_admin, _ = Group.objects.get_or_create(name="admin")
grupo_normal, _ = Group.objects.get_or_create(name="normal")
grupo_viewer, _ = Group.objects.get_or_create(name="viewer")

# 2. Permisos de Django sobre Registro, uno por rol.
# Esto es lo que usa el panel /admin/ para decidir qué botones mostrarle
# a cada quien: no hay que programar nada más, ModelAdmin ya los respeta.
content_type = ContentType.objects.get_for_model(Registro)
permisos = {
    p.codename: p
    for p in Permission.objects.filter(content_type=content_type)
}
# admin: puede ver, crear, editar y eliminar
grupo_admin.permissions.set([
    permisos["view_registro"],
    permisos["add_registro"],
    permisos["change_registro"],
    permisos["delete_registro"],
])
# normal: puede ver y crear, no editar ni eliminar (igual que en las vistas propias)
grupo_normal.permissions.set([
    permisos["view_registro"],
    permisos["add_registro"],
])
# viewer: solo puede ver
grupo_viewer.permissions.set([permisos["view_registro"]])


def crear_o_actualizar_usuario(username, password_var, grupo):
    """Crea el usuario si no existe; si ya existe, solo le actualiza el
    grupo y is_staff (para no pisarle una contraseña que ya usa)."""
    usuario, creado = User.objects.get_or_create(
        username=username, defaults={"is_staff": True}
    )
    if creado:
        usuario.set_password(config(password_var))
    usuario.is_staff = True  # necesario para poder entrar a /admin/
    usuario.save()
    usuario.groups.set([grupo])
    return creado


creado = crear_o_actualizar_usuario("admin1", "PASS_ADMIN", grupo_admin)
print("Usuario admin1", "creado" if creado else "actualizado", "(rol admin).")

creado = crear_o_actualizar_usuario("normal1", "PASS_NORMAL", grupo_normal)
print("Usuario normal1", "creado" if creado else "actualizado", "(rol normal).")

creado = crear_o_actualizar_usuario("viewer1", "PASS_VIEWER", grupo_viewer)
print("Usuario viewer1", "creado" if creado else "actualizado", "(rol viewer).")

