from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from solucion import evaluar_admision
from .models import Registro
from .decorators import requiere_rol, tiene_rol


def _cupos_ocupados(excluir_pk=None):
    ocupados = Registro.objects.filter(
        estado="Aceptado", 
        eliminado=False,
        fecha__date=timezone.localdate() # <- El filtro exigido
    )
    if excluir_pk is not None:
        ocupados = ocupados.exclude(pk=excluir_pk)
    return ocupados.count()


# ---------- READ ----------
@login_required(login_url="login")
def lista(request):  # cualquier usuario logueado puede mirar
    registros = Registro.objects.filter(eliminado=False)
    contexto = {
        "registros": registros,
        # Esto solo oculta o muestra botones en la plantilla. La
        # restricción real está en el decorador @requiere_rol de cada
        # vista: aunque alguien escriba la URL a mano, igual lo rechaza.
        "puede_crear": tiene_rol(request.user, "admin", "normal"),
        "puede_editar": tiene_rol(request.user, "admin"),
    }
    return render(request, "list.html", contexto)


# ---------- CREATE ----------
@requiere_rol("admin", "normal")
def crear(request):
    error = None
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        try:
            peso = int(request.POST.get("peso", ""))
        except ValueError:
            error = "El peso debe ser un número entero."
        else:
            if not nombre:
                error = "El nombre no puede quedar en blanco."
            else:
                mascotas_ingresadas = _cupos_ocupados()
                estado, motivo = evaluar_admision(mascotas_ingresadas, peso)
                Registro.objects.create(
                    nombre=nombre, peso=peso, estado=estado, motivo=motivo
                )
                return redirect("lista")
    return render(request, "form.html", {"accion": "Registrar", "error": error})


# ---------- UPDATE ----------
@requiere_rol("admin")
def editar(request, pk):
    reg = get_object_or_404(Registro, pk=pk, eliminado=False)
    error = None
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        try:
            peso = int(request.POST.get("peso", ""))
        except ValueError:
            error = "El peso debe ser un número entero."
        else:
            if not nombre:
                error = "El nombre no puede quedar en blanco."
            else:
                mascotas_ingresadas = _cupos_ocupados(excluir_pk=reg.pk)
                # Se recalcula con la regla de decisión: si cambia el peso,
                # el estado y el motivo tienen que quedar al día.
                estado, motivo = evaluar_admision(mascotas_ingresadas, peso)
                reg.nombre = nombre
                reg.peso = peso
                reg.estado = estado
                reg.motivo = motivo
                reg.save()
                return redirect("lista")
    return render(
        request, "form.html", {"accion": "Editar", "registro": reg, "error": error}
    )


# ---------- DELETE (lógico) ----------
@requiere_rol("admin")
def eliminar(request, pk):
    reg = get_object_or_404(Registro, pk=pk, eliminado=False)
    if request.method == "POST":
        reg.soft_delete()  # no se borra la fila, solo se marca eliminado=True
        return redirect("lista")
    return render(request, "confirm.html", {"registro": reg})


# ---------- LOGIN / LOGOUT ----------
def vista_login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", ""),
        )
        if user:
            login(request, user)
            next_url = request.GET.get("next", "lista")
            return redirect(next_url)
        messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "login.html")


def vista_logout(request):
    logout(request)
    return redirect("login")