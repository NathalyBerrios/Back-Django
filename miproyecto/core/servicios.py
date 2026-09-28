from django.utils import timezone

from .models import Registro


def cupos_ocupados(excluir_pk=None):
    """Cuántas mascotas fueron Aceptadas HOY (y no están eliminadas).

    excluir_pk se usa al editar: el registro que se está editando no debe
    contarse a sí mismo, porque su estado se va a recalcular.
    """
    ocupados = Registro.objects.filter(
        estado="Aceptado",
        eliminado=False,
        fecha__date=timezone.localdate(),  # solo cuenta las de hoy
    )
    if excluir_pk is not None:
        ocupados = ocupados.exclude(pk=excluir_pk)
    return ocupados.count()