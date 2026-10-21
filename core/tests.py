from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .models import Modalidade, Turma


class BaseTeste(TestCase):
    def setUp(self):
        call_command("carregar_dados", verbosity=0)


class ModelosTests(BaseTeste):
    def test_str_da_turma_e_legivel(self):
        turma = Turma.objects.get(modalidade__nome="Pilates", dia_semana=1)
        self.assertEqual(str(turma), "Pilates — Segunda 07:30")

    def test_nao_exclui_modalidade_com_turmas(self):  # RN03
        with self.assertRaises(ProtectedError):
            Modalidade.objects.get(nome="Musculação").delete()

    def test_exclui_modalidade_sem_turmas(self):
        Modalidade.objects.get(nome="Natação").delete()
        self.assertFalse(Modalidade.objects.filter(nome="Natação").exists())

    def test_nome_de_modalidade_unico(self):  # RN07
        with self.assertRaises(ValidationError):
            Modalidade(nome="Pilates").full_clean()

    def test_vagas_negativas_invalidas(self):  # RN06
        turma = Turma(modalidade=Modalidade.objects.get(nome="Pilates"), dia_semana=1,
                      horario="08:00", instrutor="X", vagas=-1)
        with self.assertRaises(ValidationError):
            turma.full_clean()

    def test_dia_fora_da_lista_invalido(self):  # RN04
        turma = Turma(modalidade=Modalidade.objects.get(nome="Pilates"), dia_semana=7,
                      horario="08:00", instrutor="X")
        with self.assertRaises(ValidationError):
            turma.full_clean()

    def test_turma_sem_modalidade_invalida(self):  # RN02
        with self.assertRaises(ValidationError):
            Turma(dia_semana=1, horario="08:00", instrutor="X").full_clean()

    def test_vagas_padrao_10(self):
        self.assertEqual(Turma._meta.get_field("vagas").default, 10)


class PaginasTests(BaseTeste):
    def test_home_mostra_ativas_e_nao_mostra_natacao(self):  # RF06, RN08
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        for nome in ("Musculação", "Pilates", "Funcional"):
            self.assertContains(r, nome)
        self.assertContains(r, "Solo e aparelhos, turmas pequenas")
        self.assertNotContains(r, "Natação")
        self.assertContains(r, "Academia Corpo em Movimento")

    def test_grade_na_ordem_correta(self):  # RF07
        r = self.client.get("/turmas/")
        self.assertEqual(
            [str(t) for t in r.context["turmas"]],
            ["Pilates — Segunda 07:30", "Musculação — Segunda 19:00", "Funcional — Terça 06:30",
             "Musculação — Terça 18:00", "Pilates — Quarta 07:30", "Funcional — Sábado 09:00"],
        )
        self.assertContains(r, "19:00")

    def test_menu_liga_as_duas_paginas(self):  # RF08
        self.assertContains(self.client.get("/"), reverse("turmas"))
        self.assertContains(self.client.get("/turmas/"), 'href="/"')


class PainelTests(BaseTeste):
    def setUp(self):
        super().setUp()
        get_user_model().objects.create_superuser("admin", "a@a.com", "senha123")
        self.client.login(username="admin", password="senha123")

    def test_lista_de_turmas_com_colunas(self):  # RF03
        r = self.client.get("/admin/core/turma/")
        for coluna in ("Modalidade", "Dia da semana", "Horário", "Instrutor", "Vagas"):
            self.assertContains(r, coluna)

    def test_busca_por_instrutor(self):  # RF04
        r = self.client.get("/admin/core/turma/", {"q": "Carla"})
        self.assertEqual(r.context["cl"].result_count, 2)

    def test_filtros_por_modalidade_e_dia(self):  # RF04
        pilates = Modalidade.objects.get(nome="Pilates")
        r = self.client.get("/admin/core/turma/", {"modalidade__id__exact": pilates.pk})
        self.assertEqual(r.context["cl"].result_count, 2)
        r = self.client.get("/admin/core/turma/", {"dia_semana__exact": 1})
        self.assertEqual(r.context["cl"].result_count, 2)

    def test_filtro_ativa_inativa(self):  # RF05
        r = self.client.get("/admin/core/modalidade/", {"ativa__exact": 0})
        self.assertEqual(r.context["cl"].result_count, 1)

    def test_painel_impede_excluir_musculacao(self):  # RN03
        m = Modalidade.objects.get(nome="Musculação")
        r = self.client.post(f"/admin/core/modalidade/{m.pk}/delete/", {"post": "yes"})
        self.assertTrue(Modalidade.objects.filter(pk=m.pk).exists())
        self.assertNotEqual(r.status_code, 302)
