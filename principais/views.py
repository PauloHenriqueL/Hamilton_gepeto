from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms, serializers
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission
from django.db.models import Q
from django.http import JsonResponse
from .models import Paciente
from django.views.decorators.http import require_GET
from decimal import Decimal


@require_GET
def paciente_valor_sessao(request, pk):
    """Endpoint para obter o valor da sessão de um paciente"""
    try:
        paciente = Paciente.objects.get(pk=pk)
        # Retornar o valor da sessão como um inteiro
        return JsonResponse({'vlr_sessao': int(paciente.vlr_sessao)})
    except Paciente.DoesNotExist:
        return JsonResponse({'error': 'Paciente não encontrado'}, status=404)


class ConsultaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Consulta
    template_name = 'consulta_list.html'
    context_object_name = 'consultas'
    paginate_by = 10
    permission_required = 'principais.view_consulta'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Corrigido: filtrando pelo campo fk_paciente__nome ou fk_terapeuta__nome
        nome = self.request.GET.get('nome')
        if nome:
            # Busca por nome do paciente ou terapeuta
            queryset = queryset.filter(
                models.Q(fk_paciente__nome__icontains=nome) | 
                models.Q(fk_terapeuta__nome__icontains=nome)
            )
        return queryset


class ConsultaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Consulta
    template_name = 'consulta_create.html'
    form_class = forms.ConsultaForm
    success_url = reverse_lazy('consulta-list')
    permission_required = 'principais.add_consulta'

    def form_valid(self, form):
        # Obtém os dados do formulário
        quantidade = int(self.request.POST.get('quantidade', 1))
        vlr_pix_total_str = self.request.POST.get('vlr_pix_total', '')
        
        # Converter para float se não estiver vazio
        vlr_pix_total = float(vlr_pix_total_str) if vlr_pix_total_str and vlr_pix_total_str.strip() else None
        
        # Calcular valor pago por consulta, se houver valor do pix
        vlr_pago_por_consulta = None
        
        if vlr_pix_total:
            vlr_pago_por_consulta = round(vlr_pix_total / quantidade, 2)
        
        # Cria a instância base sem salvar
        consulta = form.save(commit=False)
        
        # Verifica se a primeira consulta foi realizada
        consulta.is_realizado = self.request.POST.get('is_realizado_0', '') == 'on'
        
        # Define pagamento baseado no valor do pix E se a consulta foi realizada
        if not consulta.is_realizado:
            consulta.is_pago = False
            consulta.vlr_pago = None
        else:
            consulta.is_pago = vlr_pago_por_consulta is not None
            consulta.vlr_pago = vlr_pago_por_consulta
        
        # Verifica se há uma data específica para a primeira consulta
        if 'data_consulta_0' in self.request.POST and self.request.POST['data_consulta_0']:
            consulta.data = self.request.POST['data_consulta_0']
        
        # Salva a primeira consulta
        consulta.save()
        
        # Cria consultas adicionais se quantidade > 1
        if quantidade > 1:
            for i in range(1, quantidade):
                # Cria uma nova instância com os mesmos dados
                nova_consulta = models.Consulta(
                    fk_decano=consulta.fk_decano,
                    fk_terapeuta=consulta.fk_terapeuta,
                    fk_paciente=consulta.fk_paciente,
                    vlr_consulta=consulta.vlr_consulta,
                )
                
                # Verifica se a consulta foi realizada
                is_realizado_key = f'is_realizado_{i}'
                nova_consulta.is_realizado = self.request.POST.get(is_realizado_key, '') == 'on'
                
                # Define pagamento baseado no valor do pix E se a consulta foi realizada
                if not nova_consulta.is_realizado:
                    nova_consulta.is_pago = False
                    nova_consulta.vlr_pago = None
                else:
                    nova_consulta.is_pago = vlr_pago_por_consulta is not None
                    nova_consulta.vlr_pago = vlr_pago_por_consulta
                
                # Se houver datas específicas para cada consulta
                data_key = f'data_consulta_{i}'
                if data_key in self.request.POST and self.request.POST[data_key]:
                    nova_consulta.data = self.request.POST[data_key]
                
                nova_consulta.save()
        
        return redirect(self.success_url)


class ConsultaDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Consulta
    template_name = 'consulta_detail.html'
    permission_required = 'principais.view_consulta'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consulta = self.object
        
        # Calcular a diferença entre valor pago e valor da consulta
        if consulta.is_pago and consulta.vlr_pago is not None and consulta.vlr_consulta is not None:
            context['diferenca_valor'] = consulta.vlr_pago - consulta.vlr_consulta
        else:
            context['diferenca_valor'] = Decimal('0.00')
            
        return context

class ConsultaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Consulta
    template_name = 'consulta_update.html'
    form_class = forms.ConsultaForm
    success_url = reverse_lazy('consulta-list')
    permission_required = 'principais.change_consulta'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name in ['quantidade', 'vlr_pix_total']:
            if field_name in form.fields:
                del form.fields[field_name]
        return form


class ConsultaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Consulta
    template_name = 'consulta_delete.html'
    success_url = reverse_lazy('consulta-list')
    permission_required = 'principais.delete_consulta'


# API Views - Padronizados os nomes e adicionadas permissões consistentes

class ConsultaListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Consulta.objects.all()
    serializer_class = serializers.ConsultaSerializer
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)


class ConsultaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Consulta.objects.all()
    serializer_class = serializers.ConsultaSerializer
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)


class DecanoListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Decano.objects.all()
    serializer_class = serializers.DecanoSerializer


class DecanoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Decano.objects.all()
    serializer_class = serializers.DecanoSerializer


class PacienteListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Paciente.objects.all()
    serializer_class = serializers.PacienteSerializer


class PacienteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Paciente.objects.all()
    serializer_class = serializers.PacienteSerializer


class TerapeutaListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Terapeuta.objects.all()
    serializer_class = serializers.TerapeutaSerializer


class TerapeutaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Terapeuta.objects.all()
    serializer_class = serializers.TerapeutaSerializer