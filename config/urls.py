from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Corpo em Movimento - Painel"
admin.site.site_title = "Corpo em Movimento"
admin.site.index_title = "Gerenciar modalidades e turmas"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
