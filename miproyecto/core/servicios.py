from django.utils import timezone

from .models import Registro


def cupos_ocupados(excluir_pk=None):

    ocupados = Registro.objects.filter(
        estado="Aceptado",
        eliminado=False,
        fecha__date=timezone.localdate(),  # solo cuenta las de hoy
    )
    if excluir_pk is not None:
        ocupados = ocupados.exclude(pk=excluir_pk)
    return ocupados.count()