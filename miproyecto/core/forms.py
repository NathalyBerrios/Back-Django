from django import forms

from .models import Registro


class RegistroForm(forms.ModelForm):
    """
    Un solo lugar para validar nombre y peso, en vez de repetir el mismo
    try/except en crear() y en editar().

    estado y motivo no van en este formulario: esos los calcula la regla
    de decisión (evaluar_admision), no la persona que llena el
    formulario, así que se completan en la vista después de validar.
    """

    peso = forms.IntegerField(
        error_messages={
            "required": "El peso debe ser un número entero.",
            "invalid": "El peso debe ser un número entero.",
        }
    )

    class Meta:
        model = Registro
        fields = ["nombre", "peso"]

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "").strip()
        if not nombre:
            raise forms.ValidationError("El nombre no puede quedar en blanco.")
        return nombre

    def primer_error(self):
        """El primer mensaje de error, para mostrarlo en form.html tal
        como se mostraba antes (una sola línea de error)."""
        for errores in self.errors.values():
            return errores[0]
        return None
