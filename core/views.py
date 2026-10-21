from django.conf import settings
from django.shortcuts import render

from .models import Modalidade, Turma


def home(request):
    """Página inicial: dados da academia e modalidades ativas (RF06, RN08)."""
    contexto = {
        "academia": settings.ACADEMIA,
        "modalidades": Modalidade.objects.filter(ativa=True),
    }
    return render(request, "core/home.html", contexto)


def turmas(request):
    """Grade de turmas ordenada por dia e horário (RF07)."""
    contexto = {
        "academia": settings.ACADEMIA,
        "turmas": Turma.objects.select_related("modalidade").order_by("dia_semana", "horario"),
    }
    return render(request, "core/turmas.html", contexto)
