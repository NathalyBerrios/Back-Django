from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from solucion import CUPOS_TOTALES, evaluar_admision  # tu regla, sin reescribir
from .models import Registro
from .permissions import PermisoPorRol
from .serializers import CuposSerializer, RegistroSerializer
from .servicios import cupos_ocupados


class RegistroViewSet(viewsets.ModelViewSet):

    serializer_class = RegistroSerializer
    permission_classes = [PermisoPorRol]

    def get_queryset(self):
        # Como el filtro está aquí, un registro eliminado también responde
        # 404 si alguien pide su id directo (GET /api/registros/7/).
        return Registro.objects.filter(eliminado=False).order_by("-fecha", "-id")

    def perform_create(self, serializer):
        """El estado NO viene del cliente: lo decide la regla de decisión."""
        peso = serializer.validated_data["peso"]
        estado, motivo = evaluar_admision(cupos_ocupados(), peso)
        serializer.save(estado=estado, motivo=motivo)

    def perform_update(self, serializer):
        """Si cambia el peso, el estado y el
        motivo se recalculan. El registro que se edita no se cuenta a sí
        mismo en los cupos."""
        registro = serializer.instance
        # En PATCH puede que el cliente no mande el peso: se usa el actual.
        peso = serializer.validated_data.get("peso", registro.peso)
        estado, motivo = evaluar_admision(
            cupos_ocupados(excluir_pk=registro.pk), peso
        )
        serializer.save(estado=estado, motivo=motivo)

    def perform_destroy(self, instance):
        """Borrado lógico, como en la ES2: no se borra la fila, solo se
        marca eliminado=True. La respuesta sigue siendo 204."""
        instance.soft_delete()

    @extend_schema(responses=CuposSerializer)
    @action(detail=False, methods=["get"])
    def cupos(self, request):
        """GET /api/registros/cupos/ -> cuántos cupos quedan hoy.
        Solo lee (no modifica nada), como corresponde a un GET."""
        ocupados = cupos_ocupados()
        datos = {
            "cupos_totales": CUPOS_TOTALES,
            "ocupados_hoy": ocupados,
            "disponibles": max(CUPOS_TOTALES - ocupados, 0),
        }
        return Response(datos, status=status.HTTP_200_OK)
