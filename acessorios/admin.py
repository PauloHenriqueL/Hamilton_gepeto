from django.contrib import admin
from django.utils.html import format_html
from .models import Nucleo, Captacao, Clinica, Modalidade, Abordagem, Prefeidade


class IsActiveFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Ativos'),
            ('inactive', 'Inativos'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        if self.value() == 'inactive':
            return queryset.filter(is_active=False)


@admin.register(Clinica)
class ClinicaAdmin(admin.ModelAdmin):
    list_display = ('clinica', 'terapeutas_count', 'created_at', 'updated_at')
    search_fields = ('clinica',)
    readonly_fields = ('created_at', 'updated_at', 'terapeutas_count')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('clinica',)
        }),
        ('Estatísticas', {
            'fields': ('terapeutas_count',),
        }),
        ('Datas do Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'created_at'
    
    def terapeutas_count(self, obj):
        # Importação aqui para evitar importação circular
        from principais.models import Terapeuta
        return Terapeuta.objects.filter(fk_clinica=obj).count()
    terapeutas_count.short_description = 'Total de Terapeutas'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Em modo de edição
            return self.readonly_fields
        return ('created_at', 'updated_at')  # Em modo de criação


@admin.register(Captacao)
class CaptacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status_ativo', 'pacientes_count', 'created_at', 'updated_at')
    list_filter = (IsActiveFilter,)
    search_fields = ('nome',)
    readonly_fields = ('created_at', 'updated_at', 'pacientes_count')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'is_active')
        }),
        ('Estatísticas', {
            'fields': ('pacientes_count',),
        }),
        ('Datas do Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'created_at'
    
    def status_ativo(self, obj):
        if obj.is_active:
            return format_html('<span style="color:green;font-weight:bold;">✓ Ativo</span>')
        return format_html('<span style="color:red;font-weight:bold;">✗ Inativo</span>')
    status_ativo.short_description = 'Status'
    
    def pacientes_count(self, obj):
        # Importação aqui para evitar importação circular
        from principais.models import Paciente
        return Paciente.objects.filter(fk_captacao=obj).count()
    pacientes_count.short_description = 'Total de Pacientes'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Em modo de edição
            return self.readonly_fields
        return ('created_at', 'updated_at')  # Em modo de criação


@admin.register(Nucleo)
class NucleoAdmin(admin.ModelAdmin):
    list_display = ('nucleo', 'terapeutas_count', 'created_at', 'updated_at')
    search_fields = ('nucleo',)
    readonly_fields = ('created_at', 'updated_at', 'terapeutas_count')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nucleo',)
        }),
        ('Estatísticas', {
            'fields': ('terapeutas_count',),
        }),
        ('Datas do Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'created_at'
    
    def terapeutas_count(self, obj):
        # Importação aqui para evitar importação circular
        from principais.models import Terapeuta
        return Terapeuta.objects.filter(fk_nucleo=obj).count()
    terapeutas_count.short_description = 'Total de Terapeutas'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Em modo de edição
            return self.readonly_fields
        return ('created_at', 'updated_at')  # Em modo de criação


@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ('modalidade', 'terapeutas_count', 'created_at', 'updated_at')
    search_fields = ('modalidade',)
    readonly_fields = ('created_at', 'updated_at', 'terapeutas_count')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('modalidade',)
        }),
        ('Estatísticas', {
            'fields': ('terapeutas_count',),
        }),
        ('Datas do Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'created_at'
    
    def terapeutas_count(self, obj):
        # Importação aqui para evitar importação circular
        from principais.models import Terapeuta
        return Terapeuta.objects.filter(fk_modalidade=obj).count()
    terapeutas_count.short_description = 'Total de Terapeutas'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Em modo de edição
            return self.readonly_fields
        return ('created_at', 'updated_at')  # Em modo de criação


@admin.register(Abordagem)
class AbordagemAdmin(admin.ModelAdmin):
    list_display = ('abordagem', 'terapeutas_count', 'created_at', 'updated_at')
    search_fields = ('abordagem',)
    readonly_fields = ('created_at', 'updated_at', 'terapeutas_count')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('abordagem',)
        }),
        ('Estatísticas', {
            'fields': ('terapeutas_count',),
        }),
        ('Datas do Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'created_at'
    
    def terapeutas_count(self, obj):
        # Importação aqui para evitar importação circular
        from principais.models import Terapeuta
        return Terapeuta.objects.filter(fk_abordagem=obj).count()
    terapeutas_count.short_description = 'Total de Terapeutas'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Em modo de edição
            return self.readonly_fields
        return ('created_at', 'updated_at')  # Em modo de criação


@admin.register(Prefeidade)
class PrefeidadeAdmin(admin.ModelAdmin):
    list_display = ('terapeuta_nome', 'faixas_etarias_display', 'created_at', 'updated_at')
    list_filter = ('is_infantil', 'is_adolescente', 'is_adulto', 'is_idoso')
    search_fields = ('fk_terapeuta__nome',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Terapeuta', {
            'fields': ('fk_terapeuta',)
        }),
        ('Faixas Etárias', {
            'fields': ('is_infantil', 'is_adolescente', 'is_adulto', 'is_idoso'),
            'description': 'Selecione as faixas etárias que o terapeuta atende'
        }),
        ('Datas do Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'created_at'
    
    def terapeuta_nome(self, obj):
        if obj.fk_terapeuta:
            return obj.fk_terapeuta.nome
        return '-'
    terapeuta_nome.short_description = 'Terapeuta'
    terapeuta_nome.admin_order_field = 'fk_terapeuta__nome'
    
    def faixas_etarias_display(self, obj):
        faixas = []
        if obj.is_infantil:
            faixas.append(format_html('<span style="background-color:#E6F3FF;padding:3px 8px;border-radius:10px;margin:2px;display:inline-block;">Infantil</span>'))
        if obj.is_adolescente:
            faixas.append(format_html('<span style="background-color:#E6FFF3;padding:3px 8px;border-radius:10px;margin:2px;display:inline-block;">Adolescente</span>'))
        if obj.is_adulto:
            faixas.append(format_html('<span style="background-color:#FFF3E6;padding:3px 8px;border-radius:10px;margin:2px;display:inline-block;">Adulto</span>'))
        if obj.is_idoso:
            faixas.append(format_html('<span style="background-color:#FFE6E6;padding:3px 8px;border-radius:10px;margin:2px;display:inline-block;">Idoso</span>'))
        
        if not faixas:
            return format_html('<span style="color:gray;">Nenhuma faixa selecionada</span>')
        
        return format_html(''.join(faixas))
    faixas_etarias_display.short_description = 'Faixas Etárias'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Em modo de edição
            return self.readonly_fields
        return ('created_at', 'updated_at')  # Em modo de criação