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
