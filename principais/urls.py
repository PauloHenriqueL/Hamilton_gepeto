from django.urls import path
from . import views 

urlpatterns = [
    # URLs de Views baseadas em templates
    path('consulta/list/', views.ConsultaListView.as_view(), name='consulta-list'),
    path('consulta/create/', views.ConsultaCreateView.as_view(), name='consulta-create'),
    path('consulta/<int:pk>/detail/', views.ConsultaDetailView.as_view(), name='consulta-detail'),
    path('consulta/<int:pk>/update/', views.ConsultaUpdateView.as_view(), name='consulta-update'),
    path('consulta/<int:pk>/delete/', views.ConsultaDeleteView.as_view(), name='consulta-delete'),
    path('api/pacientes/<int:pk>/valor_sessao/', views.paciente_valor_sessao, name='paciente-valor-sessao'),
    
    path('api/v1/consulta/', views.ConsultaListCreateAPIView.as_view(), name='consulta-list-create-api'),
    path('api/v1/consulta/<int:pk>/', views.ConsultaRetrieveUpdateDestroyAPIView.as_view(), name='consulta-detail-api'),
    
    # Paciente - Padronizados os nomes e URLs
    path('api/v1/paciente/', views.PacienteListCreateAPIView.as_view(), name='paciente-list-create-api'),
    path('api/v1/paciente/<int:pk>/', views.PacienteRetrieveUpdateDestroyAPIView.as_view(), name='paciente-detail-api'),
    
    # Terapeuta - Padronizados os nomes e URLs
    path('api/v1/terapeuta/', views.TerapeutaListCreateAPIView.as_view(), name='terapeuta-list-create-api'),
    path('api/v1/terapeuta/<int:pk>/', views.TerapeutaRetrieveUpdateDestroyAPIView.as_view(), name='terapeuta-detail-api'),
    
    # Decano - Padronizados os nomes e URLs
    path('api/v1/decano/', views.DecanoListCreateAPIView.as_view(), name='decano-list-create-api'),
    path('api/v1/decano/<int:pk>/', views.DecanoRetrieveUpdateDestroyAPIView.as_view(), name='decano-detail-api'),
]