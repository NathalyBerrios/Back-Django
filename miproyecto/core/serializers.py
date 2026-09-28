from rest_framework import serializers

from .models import Registro


class RegistroSerializer(serializers.ModelSerializer):


    class Meta:
        model = Registro
        # Se enumeran a mano (nunca "__all__") para no exponer por error
        # campos internos como "eliminado" o "fecha_eliminacion".
        fields = ["id", "nombre", "peso", "estado", "motivo", "fecha"]
        read_only_fields = ["estado", "motivo", "fecha"]
        # Mensajes en español, iguales a los del RegistroForm de la ES2.
        extra_kwargs = {
            "nombre": {
                "error_messages": {
                    "blank": "El nombre no puede quedar en blanco.",
                    "required": "El nombre es obligatorio.",
                    "null": "El nombre es obligatorio.",
                }
            },
            "peso": {
                "error_messages": {
                    "invalid": "El peso debe ser un número entero.",
                    "required": "El peso debe ser un número entero.",
                    "null": "El peso debe ser un número entero.",
                }
            },
        }



class CuposSerializer(serializers.Serializer):
    """Solo describe la respuesta de /api/registros/cupos/ para la
    documentación (Swagger). No guarda nada en la base."""

    cupos_totales = serializers.IntegerField()
    ocupados_hoy = serializers.IntegerField()
    disponibles = serializers.IntegerField()
