from decouple import config
from django.contrib.auth.models import User, Group

# 1. Los tres roles que pide la pauta
for nombre in ("admin", "normal", "viewer"):
    Group.objects.get_or_create(name=nombre)

grupo_admin = Group.objects.get(name="admin")
grupo_normal = Group.objects.get(name="normal")
grupo_viewer = Group.objects.get(name="viewer")

# 2. Un usuario de ejemplo por rol (solo si no existen todavía)
if not User.objects.filter(username="admin1").exists():
    u = User.objects.create_user("admin1", password=config("PASS_ADMIN"))
    u.groups.add(grupo_admin)
    print("Usuario admin1 creado (rol admin).")

if not User.objects.filter(username="normal1").exists():
    u = User.objects.create_user("normal1", password=config("PASS_NORMAL"))
    u.groups.add(grupo_normal)
    print("Usuario normal1 creado (rol normal).")

if not User.objects.filter(username="viewer1").exists():
    u = User.objects.create_user("viewer1", password=config("PASS_VIEWER"))
    u.groups.add(grupo_viewer)
    print("Usuario viewer1 creado (rol viewer).")
