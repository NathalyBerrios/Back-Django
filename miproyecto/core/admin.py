from django import forms
from django.contrib import admin

from .models import Registro


class RegistroAdminForm(forms.ModelForm):

    class Meta:
        model = Registro
        fields = "__all__"

    def clean_peso(self):
        peso = self.cleaned_data["peso"]
        if peso < 0:
            raise forms.ValidationError("El peso no puede ser negativo.")
        return peso


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    form = RegistroAdminForm
    list_display = ("nombre", "estado", "peso", "motivo", "fecha", "eliminado")
    list_filter = ("estado", "eliminado")
    search_fields = ("nombre",)
    readonly_fields = ("fecha_eliminacion",)

    # --- Permisos por usuario dentro del panel ---
    # No hace falta reescribir has_add_permission/has_change_permission/
    # has_delete_permission a mano: ModelAdmin ya los consulta solo con
    # request.user.has_perm("core.add_registro"), etc. Lo único que falta
    # es asignarle esos permisos a cada Group, lo que se hace en
    # crear_usuarios.py (admin: los 4 permisos; normal: ver y crear;
    # viewer: solo ver). Así, por ejemplo, viewer1 puede entrar a
    # /admin/ y mirar, pero no ve los botones de crear/editar/eliminar.

