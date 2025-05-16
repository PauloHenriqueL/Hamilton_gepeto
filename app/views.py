import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import metrics


@login_required(login_url='login')
def dashboard(request):
    consulta_metrics = metrics.get_consulta_metrics()
    terapeuta_metrics = metrics.get_terapeuta_metrics()
    daily_consultas_data = metrics.get_daily_consultas_data()
    daily_valor_data = metrics.get_daily_valor_data()
    consultas_status = metrics.get_consultas_por_status()
    pacientes_ativos = metrics.get_pacientes_ativos()
    
    # Novas métricas mensais
    monthly_consultas_data = metrics.get_monthly_consultas_data()
    monthly_receita_data = metrics.get_monthly_receita_data()

    context = {
        # Métricas originais
        'consulta_metrics': consulta_metrics,
        'consultas_por_terapeuta': json.dumps(terapeuta_metrics['consultas_por_terapeuta']),
        'valor_por_terapeuta': json.dumps(terapeuta_metrics['valor_por_terapeuta']),
        'daily_consultas_data': json.dumps(daily_consultas_data),
        'daily_valor_data': json.dumps(daily_valor_data),
        'pagamento_status': json.dumps(consultas_status['pagamento_status']),
        'realizacao_status': json.dumps(consultas_status['realizacao_status']),
        'pacientes_ativos': json.dumps(pacientes_ativos),
        
        # Novas métricas
        'metricas_terapeutas': terapeuta_metrics['metricas_detalhadas'],
        'monthly_consultas_data': json.dumps(monthly_consultas_data),
        'monthly_receita_data': json.dumps(monthly_receita_data),
    }

    return render(request, 'home.html', context)