from django import forms
from . import models
import re
from django.core.exceptions import ObjectDoesNotExist


class ConsultaForm(forms.ModelForm):
    
    class Meta:
        model = models.Consulta
        fields = [
            'fk_decano',
            'fk_terapeuta', 
            'fk_paciente', 
            'vlr_consulta',
            'is_realizado',  
            'is_pago', 
            'vlr_pago'
        ]
        widgets = {
            'fk_decano': forms.Select(attrs={'class': 'form-control'}),
            'fk_terapeuta': forms.Select(attrs={'class': 'form-control'}),
            'fk_paciente': forms.Select(attrs={'class': 'form-control', 'id': 'paciente-select'}),
            'vlr_consulta': forms.NumberInput(attrs={'class': 'form-control', 'id': 'valor-consulta'}),
            'is_realizado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_pago': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vlr_pago': forms.NumberInput(attrs={'class': 'form-control'})
        }
        labels = {
            'title': 'Título',
            'fk_decano': 'Decano',
            'fk_terapeuta': 'Terapeuta', 
            'fk_paciente': 'Paciente', 
            'vlr_consulta': 'Valor da consulta',
            'is_realizado': 'Foi realizado?',  
            'is_pago': 'Foi pago?', 
            'vlr_pago': 'Valor pago?'
        }

    quantidade = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    vlr_pix_total = forms.DecimalField(
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        label='Valor total recebido no PIX'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Se o formulário for preenchido com dados POST e tiver paciente selecionado
        if args and isinstance(args[0], dict) and 'fk_paciente' in args[0]:
            paciente_id = args[0].get('fk_paciente')
            if paciente_id:
                try:
                    paciente = models.Paciente.objects.get(pk=paciente_id)
                    self.fields['vlr_consulta'].initial = paciente.vlr_sessao
                except ObjectDoesNotExist:
                    pass