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
    
    # ---- MÉTRICAS FINANCEIRAS ----
    
    # Preço médio acordado (média de vlr_sessao na tabela de pacientes ativos)
    preco_medio_acordado = models.Paciente.objects.filter(is_active=True).aggregate(
        avg_price=Avg('vlr_sessao')
    )['avg_price'] or Decimal('0.00')
    
    # Preço médio esperado (vlr_sessao somado da planilha de consultas / número de consultas)
    preco_medio_esperado = models.Consulta.objects.aggregate(
        avg_expected=Avg('fk_paciente__vlr_sessao')
    )['avg_expected'] or Decimal('0.00')
    
    # Preço médio realizado (valor total do pix / número de consultas realizadas)
    preco_medio_realizado = Decimal('0.00')
    if consultas_realizadas > 0:
        preco_medio_realizado = valor_total_recebido / consultas_realizadas
    
    # Receita realizada (valor total pix)
    receita_realizada = valor_total_recebido
    
    # Receita esperada (consultas * vlr_sessao na tabela de consulta)
    receita_esperada = models.Consulta.objects.aggregate(
        total=Sum('fk_paciente__vlr_sessao')
    )['total'] or Decimal('0.00')
    
    # Receita acordada (consultas * vlr_sessao no cadastramento de paciente)
    receita_acordada = Decimal('0.00')
    consultas = models.Consulta.objects.all()
    for consulta in consultas:
        if consulta.fk_paciente and consulta.fk_paciente.vlr_sessao:
            receita_acordada += consulta.fk_paciente.vlr_sessao
    
    # ---- DADOS CLÍNICOS ----
    
    # Taxa de adesão (realizados/total)
    taxa_adesao = (consultas_realizadas / total_consultas * 100) if total_consultas > 0 else 0
    
    # Total de sessões (número de sessões realizadas)
    total_sessoes = consultas_realizadas
    
    # Total de sessões do mês atual
    total_sessoes_mes = models.Consulta.objects.filter(
        data__gte=primeiro_dia_mes,
        is_realizado=True
    ).count()
    
    # ---- DADOS BRUTOS ----
    
    # Número de vendas (pacientes cadastrados nesse mês)
    vendas_mes = models.Paciente.objects.filter(
        created_at__gte=timezone.make_aware(datetime.combine(primeiro_dia_mes, datetime.min.time()))
    ).count()
    
    # Número de pacientes ativos
    pacientes_ativos_count = models.Paciente.objects.filter(is_active=True).count()
    
    # Número de terapeutas
    total_terapeutas = models.Terapeuta.objects.count()
    
    # Receita total do mês
    receita_total_mes = models.Consulta.objects.filter(
        data__gte=primeiro_dia_mes,
        is_pago=True
    ).aggregate(
        total=Sum('vlr_pago')
    )['total'] or Decimal('0.00')

    return dict(
        # Métricas originais
        total_consultas=total_consultas,
        consultas_realizadas=consultas_realizadas,
        consultas_pagas=consultas_pagas,
        consultas_pendentes=consultas_pendentes,
        valor_total_consultas=number_format(valor_total_consultas, decimal_pos=2, force_grouping=True),
        valor_total_recebido=number_format(valor_total_recebido, decimal_pos=2, force_grouping=True),
        
        # Métricas financeiras
        preco_medio_acordado=number_format(preco_medio_acordado, decimal_pos=2, force_grouping=True),
        preco_medio_esperado=number_format(preco_medio_esperado, decimal_pos=2, force_grouping=True),
        preco_medio_realizado=number_format(preco_medio_realizado, decimal_pos=2, force_grouping=True),
        receita_realizada=number_format(receita_realizada, decimal_pos=2, force_grouping=True),
        receita_esperada=number_format(receita_esperada, decimal_pos=2, force_grouping=True),
        receita_acordada=number_format(receita_acordada, decimal_pos=2, force_grouping=True),
        
        # Dados clínicos
        taxa_adesao=number_format(taxa_adesao, decimal_pos=1),
        total_sessoes=total_sessoes,
        total_sessoes_mes=total_sessoes_mes,
        
        # Dados brutos
        vendas_mes=vendas_mes,
        pacientes_ativos_count=pacientes_ativos_count,
        total_terapeutas=total_terapeutas,
        
        # Receita do mês
        receita_total_mes=number_format(receita_total_mes, decimal_pos=2, force_grouping=True),
    )

def get_terapeuta_metrics():
    """Obter métricas de consultas por terapeuta"""
    terapeutas = models.Terapeuta.objects.all()
    
    # Métricas por terapeuta detalhadas
    metricas_detalhadas = []
    
    for terapeuta in terapeutas:
        # Total de consultas marcadas
        total_consultas_terapeuta = models.Consulta.objects.filter(
            fk_terapeuta=terapeuta
        ).count()
        
        # Total de consultas realizadas
        total_consultasrealizadas_terapeuta = models.Consulta.objects.filter(
            fk_terapeuta=terapeuta,
            is_realizado=True
        ).count()
        
        # Taxa de adesão (consultas realizadas / consultas marcadas)
        taxa_adesao_terapeuta = (
            total_consultasrealizadas_terapeuta / total_consultas_terapeuta * 100
        ) if total_consultas_terapeuta > 0 else 0
        
        # Número de pacientes ativos (pacientes únicos com consultas)
        pacientes_ativos_terapeuta = models.Consulta.objects.filter(
            fk_terapeuta=terapeuta
        ).values('fk_paciente').distinct().count()
        
        # Valor total recebido pelo terapeuta
        valor_recebido_terapeuta = models.Consulta.objects.filter(
            fk_terapeuta=terapeuta,
            is_pago=True
        ).aggregate(
            total=Sum('vlr_pago')
        )['total'] or Decimal('0.00')
        
        # Receita esperada do terapeuta
        receita_esperada_terapeuta = models.Consulta.objects.filter(
            fk_terapeuta=terapeuta
        ).aggregate(
            total=Sum('fk_paciente__vlr_sessao')
        )['total'] or Decimal('0.00')
        
        metricas_detalhadas.append({
            'nome': terapeuta.nome,
            'taxa_adesao': number_format(taxa_adesao_terapeuta, decimal_pos=1),
            'pacientes_ativos': pacientes_ativos_terapeuta,
            'total_consultas': total_consultas_terapeuta,
            'total_consultasrealizadas': total_consultasrealizadas_terapeuta,
            'valor_recebido': number_format(valor_recebido_terapeuta, decimal_pos=2, force_grouping=True),
            'receita_esperada': number_format(receita_esperada_terapeuta, decimal_pos=2, force_grouping=True)
        })
    
    # Retorna as métricas detalhadas para uso no template
    return metricas_detalhadas

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
    
    # Modificação: Usar nomes de chaves em minúsculas e sem acentos para consistência com o JavaScript
    pagamento_status = {
        'pago': total_pagas,
        'pendente': total_nao_pagas
    }
    
    realizacao_status = {
        'realizada': total_realizadas,
        'nao_realizada': total_nao_realizadas
    }
    
    return {
        'pagamento_status_data': pagamento_status,
        'realizacao_status_data': realizacao_status
    }

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