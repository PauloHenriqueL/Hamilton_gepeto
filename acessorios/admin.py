# avaliacao/admin.py
from django.contrib import admin
from .models import Nucleo, Captacao, Clinica, Modalidade, Abordagem, Prefeidade

@admin.register(Clinica)
class NucleoAdmin(admin.ModelAdmin):
    list_display = ('clinica',)
    search_fields = ('clinica',)

@admin.register(Captacao)
class NucleoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Nucleo)
class NucleoAdmin(admin.ModelAdmin):
    list_display = ('nucleo',)
    search_fields = ('nucleo',)

@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ('modalidade',)
    search_fields = ('modalidade',)

@admin.register(Abordagem)
class AbordagemAdmin(admin.ModelAdmin):
    list_display = ('abordagem',)
    list_filter = ('abordagem',)

@admin.register(Prefeidade)
class PrefeidadeAdmin(admin.ModelAdmin):
    list_display = ('is_infantil',)
