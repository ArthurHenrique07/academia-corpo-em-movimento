from django.contrib import admin

from .models import Modalidade, Turma


@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativa")  # RF05
    list_filter = ("ativa",)  # RF05
    search_fields = ("nome",)


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ("modalidade", "dia_semana", "horario_formatado", "instrutor", "vagas")  # RF03
    list_filter = ("modalidade", "dia_semana")  # RF04
    search_fields = ("instrutor",)  # RF04
    list_select_related = ("modalidade",)

    @admin.display(description="horário", ordering="horario")
    def horario_formatado(self, turma):
        return turma.horario.strftime("%H:%M")
