from django.db.models import Sum, Count, F, Q, Avg, Case, When, IntegerField, DecimalField
from django.db.models.functions import TruncMonth
from django.utils.formats import number_format
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from principais import models


def get_consulta_metrics():
    """Obter métricas gerais sobre consultas"""
    # Métricas originais
    total_consultas = models.Consulta.objects.count()
    consultas_realizadas = models.Consulta.objects.filter(is_realizado=True).count()
    consultas_pagas = models.Consulta.objects.filter(is_pago=True).count()
    
    valor_total_consultas = models.Consulta.objects.aggregate(
        total=Sum('vlr_consulta')
    )['total'] or 0
    
    valor_total_recebido = models.Consulta.objects.filter(is_pago=True).aggregate(
        total=Sum('vlr_pago')
    )['total'] or 0
    
    consultas_pendentes = models.Consulta.objects.filter(
        Q(is_realizado=False) | Q(is_realizado=None)
    ).count()

    # Novas métricas para a Allos
    hoje = timezone.now().date()
    primeiro_dia_mes = hoje.replace(day=1)
    
    # Preço médio da sessão
    preco_medio = models.Paciente.objects.filter(is_active=True).aggregate(
        avg_price=Avg('vlr_sessao')
    )['avg_price'] or Decimal('0.00')
    
    # Taxa de adesão (realizados/total)
    taxa_adesao = (consultas_realizadas / total_consultas * 100) if total_consultas > 0 else 0
    
    # Total de sessões (por mês)
    total_sessoes_mes = models.Consulta.objects.filter(
        data__gte=primeiro_dia_mes
    ).count()
    
    # Receita total (por mês)
    receita_total_mes = models.Consulta.objects.filter(
        data__gte=primeiro_dia_mes,
        is_pago=True
    ).aggregate(
        total=Sum('vlr_pago')
    )['total'] or Decimal('0.00')
    
    # Receita esperada (total de consultas * vlr_sessao)
    receita_esperada = models.Consulta.objects.filter(
        data__gte=primeiro_dia_mes
    ).aggregate(
        total=Sum(F('fk_paciente__vlr_sessao'))
    )['total'] or Decimal('0.00')
    
    # Número de vendas (pacientes cadastrados nesse mês)
    # Usando created_at em vez de data_cadastro
    vendas_mes = models.Paciente.objects.filter(
        created_at__gte=timezone.make_aware(datetime.combine(primeiro_dia_mes, datetime.min.time()))
    ).count()
    
    # Número de pacientes ativos
    pacientes_ativos_count = models.Paciente.objects.filter(is_active=True).count()
    
    # Número de terapeutas
    total_terapeutas = models.Terapeuta.objects.count()

    return dict(
        # Métricas originais
        total_consultas=total_consultas,
        consultas_realizadas=consultas_realizadas,
        consultas_pagas=consultas_pagas,
        consultas_pendentes=consultas_pendentes,
        valor_total_consultas=number_format(valor_total_consultas, decimal_pos=2, force_grouping=True),
        valor_total_recebido=number_format(valor_total_recebido, decimal_pos=2, force_grouping=True),
        
        # Novas métricas
        preco_medio=number_format(preco_medio, decimal_pos=2, force_grouping=True),
        taxa_adesao=number_format(taxa_adesao, decimal_pos=1),
        total_sessoes_mes=total_sessoes_mes,
        receita_total_mes=number_format(receita_total_mes, decimal_pos=2, force_grouping=True),
        receita_esperada=number_format(receita_esperada, decimal_pos=2, force_grouping=True),
        vendas_mes=vendas_mes,
        pacientes_ativos_count=pacientes_ativos_count,
        total_terapeutas=total_terapeutas,
    )

def get_terapeuta_metrics():
    """Obter métricas de consultas por terapeuta"""
    terapeutas = models.Terapeuta.objects.all()
    consultas_por_terapeuta = {}
    valor_por_terapeuta = {}
    
    # Obter data do primeiro dia do mês atual
    hoje = timezone.now().date()
    primeiro_dia_mes = hoje.replace(day=1)
    
    # Métricas por terapeuta detalhadas
    metricas_detalhadas = []
    
    for terapeuta in terapeutas:
        # Métricas originais
        consultas_count = models.Consulta.objects.filter(fk_terapeuta=terapeuta).count()
        consultas_por_terapeuta[terapeuta.nome] = consultas_count
        
        valor_total = models.Consulta.objects.filter(fk_terapeuta=terapeuta).aggregate(
            total=Sum('vlr_consulta')
        )['total'] or 0
        valor_por_terapeuta[terapeuta.nome] = float(valor_total)
        
        # Novas métricas por terapeuta
        # Taxa de adesão
        consultas_terapeuta_total = models.Consulta.objects.filter(
            fk_terapeuta=terapeuta
        ).count()
        
        consultas_terapeuta_realizadas = models.Consulta.objects.filter(
            fk_terapeuta=terapeuta,
            is_realizado=True
        ).count()
        
        taxa_adesao_terapeuta = (
            consultas_terapeuta_realizadas / consultas_terapeuta_total * 100
        ) if consultas_terapeuta_total > 0 else 0
        
        # Número de pacientes ativos
        # Aqui precisamos de uma lógica diferente, pois não há fk_terapeuta em Paciente
        # Vamos contar pacientes únicos que tiveram consultas com o terapeuta
        pacientes_ativos_terapeuta = models.Consulta.objects.filter(
            fk_terapeuta=terapeuta
        ).values('fk_paciente').distinct().count()
        
        # Número total de consultas
        total_consultas_terapeuta = models.Consulta.objects.filter(
            fk_terapeuta=terapeuta
        ).count()
        
        metricas_detalhadas.append({
            'nome': terapeuta.nome,
            'taxa_adesao': number_format(taxa_adesao_terapeuta, decimal_pos=1),
            'pacientes_ativos': pacientes_ativos_terapeuta,
            'total_consultas': total_consultas_terapeuta
        })

    return dict(
        consultas_por_terapeuta=consultas_por_terapeuta,
        valor_por_terapeuta=valor_por_terapeuta,
        metricas_detalhadas=metricas_detalhadas,
    )

def get_daily_consultas_data():
    """Obter dados diários de consultas para os últimos 7 dias"""
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    values = []

    for date in dates:
        consultas_count = models.Consulta.objects.filter(data=date).count()
        values.append(consultas_count)

    return dict(
        dates=dates,
        values=values,
    )

def get_monthly_consultas_data():
    """Obter dados mensais de consultas para os últimos 6 meses"""
    today = timezone.now().date()
    
    # Calcular o primeiro dia do mês atual e dos 5 meses anteriores
    meses = []
    valores = []
    
    for i in range(5, -1, -1):
        # Calcular o primeiro dia do mês i meses atrás
        month = today.month - i
        year = today.year
        # Ajustar o ano se necessário
        while month <= 0:
            month += 12
            year -= 1
        
        first_day = datetime(year, month, 1).date()
        # Calcular o primeiro dia do próximo mês
        if month == 12:
            next_month_first_day = datetime(year + 1, 1, 1).date()
        else:
            next_month_first_day = datetime(year, month + 1, 1).date()
        
        # Nome do mês
        meses.append(first_day.strftime('%b/%Y'))
        
        # Contar consultas neste mês
        consultas_count = models.Consulta.objects.filter(
            data__gte=first_day,
            data__lt=next_month_first_day
        ).count()
        valores.append(consultas_count)
    
    return dict(
        months=meses,
        values=valores,
    )

def get_monthly_receita_data():
    """Obter dados mensais de receita para os últimos 6 meses"""
    today = timezone.now().date()
    
    # Calcular o primeiro dia do mês atual e dos 5 meses anteriores
    meses = []
    valores = []
    
    for i in range(5, -1, -1):
        # Calcular o primeiro dia do mês i meses atrás
        month = today.month - i
        year = today.year
        # Ajustar o ano se necessário
        while month <= 0:
            month += 12
            year -= 1
        
        first_day = datetime(year, month, 1).date()
        # Calcular o primeiro dia do próximo mês
        if month == 12:
            next_month_first_day = datetime(year + 1, 1, 1).date()
        else:
            next_month_first_day = datetime(year, month + 1, 1).date()
        
        # Nome do mês
        meses.append(first_day.strftime('%b/%Y'))
        
        # Calcular receita neste mês
        receita = models.Consulta.objects.filter(
            data__gte=first_day,
            data__lt=next_month_first_day,
            is_pago=True
        ).aggregate(
            total=Sum('vlr_pago')
        )['total'] or Decimal('0.00')
        
        valores.append(float(receita))
    
    return dict(
        months=meses,
        values=valores,
    )

def get_daily_valor_data():
    """Obter dados diários de valor das consultas para os últimos 7 dias"""
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    values = []

    for date in dates:
        valor_total = models.Consulta.objects.filter(data=date).aggregate(
            total=Sum('vlr_consulta')
        )['total'] or 0
        values.append(float(valor_total))

    return dict(
        dates=dates,
        values=values,
    )

def get_consultas_por_status():
    """Obter contagem de consultas por status (pago/não pago, realizado/não realizado)"""
    total_pagas = models.Consulta.objects.filter(is_pago=True).count()
    total_nao_pagas = models.Consulta.objects.filter(Q(is_pago=False) | Q(is_pago=None)).count()
    
    total_realizadas = models.Consulta.objects.filter(is_realizado=True).count()
    total_nao_realizadas = models.Consulta.objects.filter(Q(is_realizado=False) | Q(is_realizado=None)).count()
    
    return dict(
        pagamento_status={
            'Pagas': total_pagas,
            'Não Pagas': total_nao_pagas
        },
        realizacao_status={
            'Realizadas': total_realizadas,
            'Não Realizadas': total_nao_realizadas
        }
    )

def get_pacientes_ativos():
    """Obter pacientes com mais consultas"""
    pacientes = models.Paciente.objects.all()
    consultas_por_paciente = {}
    
    for paciente in pacientes:
        consultas_count = models.Consulta.objects.filter(fk_paciente=paciente).count()
        if consultas_count > 0:  # Mostrar apenas pacientes com consultas
            consultas_por_paciente[paciente.nome] = consultas_count
    
    # Ordernar e pegar os top 5
    top_pacientes = dict(sorted(consultas_por_paciente.items(), 
                                key=lambda item: item[1], 
                                reverse=True)[:5])
    
    return top_pacientes