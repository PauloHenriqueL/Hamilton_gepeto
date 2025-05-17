import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import metrics


@login_required(login_url='login')
def dashboard(request):
    # Obter todas as métricas necessárias
    consulta_metrics = metrics.get_consulta_metrics()
    metricas_terapeutas = metrics.get_terapeuta_metrics()
    
    # Dados para gráficos
    monthly_consultas_data = metrics.get_monthly_consultas_data()
    monthly_receita_data = metrics.get_monthly_receita_data()
    daily_consultas_data = metrics.get_daily_consultas_data()
    daily_valor_data = metrics.get_daily_valor_data()
    
    # Obter dados de status - usando a função corrigida
    status_data = metrics.get_consultas_por_status()
    
    # Obter dados de pacientes ativos
    pacientes_ativos_data = metrics.get_pacientes_ativos()
    
    # Preparar dados para gráfico de terapeutas (exemplo)
    terapeuta_consultas_data = {
        'terapeutas': [t['nome'] for t in metricas_terapeutas],
        'values': [t['total_consultas'] for t in metricas_terapeutas]
    }
    
    # Converter todos os dados para JSON
    context = {
        'consulta_metrics': consulta_metrics,
        'metricas_terapeutas': metricas_terapeutas,
        'monthly_consultas_data': json.dumps(monthly_consultas_data),
        'monthly_receita_data': json.dumps(monthly_receita_data),
        'daily_consultas_data': json.dumps(daily_consultas_data),
        'daily_valor_data': json.dumps(daily_valor_data),
        'pagamento_status_data': json.dumps(status_data['pagamento_status_data']),
        'realizacao_status_data': json.dumps(status_data['realizacao_status_data']),
        'terapeuta_consultas_data': json.dumps(terapeuta_consultas_data),
        'pacientes_ativos_data': json.dumps(pacientes_ativos_data)
    }
    
    return render(request, 'home.html', context)