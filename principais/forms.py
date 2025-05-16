from django import forms
from . import models
import re


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
            'fk_paciente': forms.Select(attrs={'class': 'form-control'}),
            'vlr_consulta': forms.NumberInput(attrs={'class': 'form-control'}),
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