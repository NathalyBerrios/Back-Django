from django.db import models
from django.utils import timezone


class Registro(models.Model):
    """
    Una ficha de admisión veterinaria: el mismo dato que antes vivía como
    un diccionario dentro de datos.json, ahora como tabla en SQLite.
    """

    ESTADO_CHOICES = [
        ("Aceptado", "Aceptado"),
        ("Rechazado", "Rechazado"),
        ("Dato Inválido", "Dato Inválido"),
    ]

    nombre = models.CharField(max_length=100)
    peso = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    motivo = models.CharField(max_length=200)
    fecha = models.DateTimeField(default=timezone.now)

    # Borrado lógico: eliminar() nunca borra la fila, solo la oculta.
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.nombre} - {self.estado}"

    def soft_delete(self):
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.save()
