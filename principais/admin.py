# avaliacao/admin.py
from django.contrib import admin
from .models import Decano, Paciente, Terapeuta, Consulta

@admin.register(Decano)
class DecanoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at')
    search_fields = ('nome',)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at')
    search_fields = ('nome',)

@admin.register(Terapeuta)
class TerapeutaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at')
    list_filter = ('nome',)

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('is_realizado', 'is_pago')
    list_filter = ('is_realizado',)
