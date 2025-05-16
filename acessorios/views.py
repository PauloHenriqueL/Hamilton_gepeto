from rest_framework import generics
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class AbordagemListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Abordagem.objects.all()
    serializer_class = serializers.AbordagemSerializer  # Corrigido aqui


class AbordagemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # Corrigido o nome da classe e tipo de view
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Abordagem.objects.all()
    serializer_class = serializers.AbordagemSerializer  # Corrigido aqui


class CaptacaoListCreateAPIView(generics.ListCreateAPIView):  # Padronizado o nome da classe
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Captacao.objects.all()
    serializer_class = serializers.CaptacaoSerializer  # Corrigido aqui


class CaptacaoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # Corrigido o nome da classe e tipo de view
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Captacao.objects.all()
    serializer_class = serializers.CaptacaoSerializer  # Corrigido aqui


class ClinicaListCreateAPIView(generics.ListCreateAPIView):  # Padronizado o nome da classe
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Clinica.objects.all()
    serializer_class = serializers.ClinicaSerializer  # Corrigido aqui


class ClinicaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # Corrigido o nome da classe e tipo de view
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Clinica.objects.all()
    serializer_class = serializers.ClinicaSerializer  # Corrigido aqui


class ModalidadeListCreateAPIView(generics.ListCreateAPIView):  # Padronizado o nome da classe
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Modalidade.objects.all()
    serializer_class = serializers.ModalidadeSerializer  # Corrigido aqui


class ModalidadeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # Corrigido o nome da classe e tipo de view
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Modalidade.objects.all()
    serializer_class = serializers.ModalidadeSerializer  # Corrigido aqui


class NucleoListCreateAPIView(generics.ListCreateAPIView):  # Padronizado o nome da classe
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Nucleo.objects.all()
    serializer_class = serializers.NucleoSerializer  # Corrigido aqui


class NucleoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # Corrigido o nome da classe e tipo de view
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Nucleo.objects.all()
    serializer_class = serializers.NucleoSerializer  # Corrigido aqui


class PrefeidadeListCreateAPIView(generics.ListCreateAPIView):  # Padronizado o nome da classe
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Prefeidade.objects.all()
    serializer_class = serializers.PrefeidadeSerializer  # Corrigido aqui


class PrefeidadeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # Corrigido o nome da classe e tipo de view
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Prefeidade.objects.all()
    serializer_class = serializers.PrefeidadeSerializer  # Corrigido aqui