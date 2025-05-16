from django.urls import path
from . import views


urlpatterns = [
    # API URLs para Abordagem
    path('api/v1/abordagem/', views.AbordagemListCreateAPIView.as_view(), name='abordagem-list-create-api'),
    path('api/v1/abordagem/<int:pk>/', views.AbordagemRetrieveUpdateDestroyAPIView.as_view(), name='abordagem-detail-api'),
    
    # API URLs para Captação
    path('api/v1/captacao/', views.CaptacaoListCreateAPIView.as_view(), name='captacao-list-create-api'),
    path('api/v1/captacao/<int:pk>/', views.CaptacaoRetrieveUpdateDestroyAPIView.as_view(), name='captacao-detail-api'),
    
    # API URLs para Clínica
    path('api/v1/clinica/', views.ClinicaListCreateAPIView.as_view(), name='clinica-list-create-api'),
    path('api/v1/clinica/<int:pk>/', views.ClinicaRetrieveUpdateDestroyAPIView.as_view(), name='clinica-detail-api'),
    
    # API URLs para Modalidade
    path('api/v1/modalidade/', views.ModalidadeListCreateAPIView.as_view(), name='modalidade-list-create-api'),
    path('api/v1/modalidade/<int:pk>/', views.ModalidadeRetrieveUpdateDestroyAPIView.as_view(), name='modalidade-detail-api'),
    
    # API URLs para Núcleo
    path('api/v1/nucleo/', views.NucleoListCreateAPIView.as_view(), name='nucleo-list-create-api'),
    path('api/v1/nucleo/<int:pk>/', views.NucleoRetrieveUpdateDestroyAPIView.as_view(), name='nucleo-detail-api'),
    
    # API URLs para Preferência de Idade
    path('api/v1/prefeidade/', views.PrefeidadeListCreateAPIView.as_view(), name='prefeidade-list-create-api'),
    path('api/v1/prefeidade/<int:pk>/', views.PrefeidadeRetrieveUpdateDestroyAPIView.as_view(), name='prefeidade-detail-api'),
]