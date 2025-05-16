from rest_framework import serializers
from . import models


class AbordagemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Abordagem
        fields = '__all__'

class NucleoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Nucleo
        fields = '__all__'

class CaptacaoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Captacao
        fields = '__all__'

class ClinicaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Clinica
        fields = '__all__'

class ModalidadeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Modalidade
        fields = '__all__'

class PrefeidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Prefeidade
        fields = '__all__'