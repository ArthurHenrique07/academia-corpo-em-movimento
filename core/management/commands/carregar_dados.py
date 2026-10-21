from datetime import time

from django.core.management.base import BaseCommand

from core.models import Modalidade, Turma

MODALIDADES = [
    ("Musculação", "Treino com pesos, acompanhamento individual", True),
    ("Pilates", "Solo e aparelhos, turmas pequenas", True),
    ("Funcional", "Circuito de alta intensidade", True),
    ("Natação", "Piscina aquecida (em reforma)", False),
]

D = Turma.Dia
TURMAS = [
    ("Pilates", D.SEGUNDA, time(7, 30), "Rafael", 8),
    ("Musculação", D.SEGUNDA, time(19, 0), "Carla", 15),
    ("Funcional", D.TERCA, time(6, 30), "Diego", 12),
    ("Musculação", D.TERCA, time(18, 0), "Carla", 15),
    ("Pilates", D.QUARTA, time(7, 30), "Rafael", 8),
    ("Funcional", D.SABADO, time(9, 0), "Diego", 20),
]


class Command(BaseCommand):
    help = "Carrega os dados iniciais da academia (seção 7 do documento). Pode rodar mais de uma vez."

    def handle(self, *args, **options):
        for nome, descricao, ativa in MODALIDADES:
            Modalidade.objects.update_or_create(
                nome=nome, defaults={"descricao": descricao, "ativa": ativa}
            )
        for nome, dia, horario, instrutor, vagas in TURMAS:
            Turma.objects.update_or_create(
                modalidade=Modalidade.objects.get(nome=nome),
                dia_semana=dia,
                horario=horario,
                defaults={"instrutor": instrutor, "vagas": vagas},
            )
        if options["verbosity"] > 0:
            self.stdout.write(self.style.SUCCESS("Dados iniciais carregados."))
