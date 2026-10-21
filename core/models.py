from django.db import models


class Modalidade(models.Model):
    """Tipo de aula oferecido (Pilates, Musculação...)."""

    nome = models.CharField("nome", max_length=80, unique=True)  # RN07
    descricao = models.TextField("descrição", blank=True)
    ativa = models.BooleanField("ativa", default=True)  # RN08

    class Meta:
        verbose_name = "modalidade"
        verbose_name_plural = "modalidades"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Turma(models.Model):
    """Aula de uma modalidade em um dia e horário, com um instrutor."""

    class Dia(models.IntegerChoices):  # RN04: lista fixa, segunda a sábado
        SEGUNDA = 1, "Segunda"
        TERCA = 2, "Terça"
        QUARTA = 3, "Quarta"
        QUINTA = 4, "Quinta"
        SEXTA = 5, "Sexta"
        SABADO = 6, "Sábado"

    # PROTECT impede excluir uma modalidade que tenha turmas (RN03).
    # Campo obrigatório (sem null=True) garante que não existe turma sem modalidade (RN02).
    modalidade = models.ForeignKey(
        Modalidade,
        on_delete=models.PROTECT,
        related_name="turmas",
        verbose_name="modalidade",
    )
    dia_semana = models.PositiveSmallIntegerField("dia da semana", choices=Dia.choices)
    horario = models.TimeField("horário")  # RN05: 24h, ex.: 07:30
    instrutor = models.CharField("instrutor", max_length=100)
    vagas = models.PositiveIntegerField("vagas", default=10)  # RN06: inteiro >= 0

    class Meta:
        verbose_name = "turma"
        verbose_name_plural = "turmas"
        ordering = ["dia_semana", "horario"]  # RF07

    def __str__(self):
        # Identificação legível, ex.: "Pilates — Segunda 07:30"
        return f"{self.modalidade.nome} — {self.get_dia_semana_display()} {self.horario:%H:%M}"
