from django.db import models
from django.utils import timezone
from acessorios.models import Abordagem, Nucleo, Clinica, Modalidade, Captacao



class Decano(models.Model):
    pk_decano = models.AutoField(primary_key=True, verbose_name="ID")
    nome = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone", help_text="Exemplo: 31988553344 Não coloque +55/espaços/parênteses")
    dat_nascimento = models.DateField(verbose_name="Data de Nascimento")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        ordering = ['nome']
        db_table = '"hamilton"."decanos"'
        verbose_name = "Decano"
        verbose_name_plural = "Decanos"
   
    def __str__(self):
        return self.nome

class Paciente(models.Model):
    pk_paciente = models.AutoField(primary_key=True, verbose_name="ID")
    fk_captacao = models.ForeignKey(
        Captacao,  # Usando a classe importada corretamente
        on_delete=models.CASCADE, 
        db_column='fk_captacao',
        verbose_name="Captação"
    )
    nome = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone do Paciente", help_text="Exemplo: 31988553344 Não coloque +55/espaços/parênteses")
    nome_contato_apoio = models.CharField(null=True, blank=True, max_length=200, verbose_name="Nome do Contato de Apoio")
    parentesco_contato_apoio = models.CharField(null=True, blank=True, max_length=200, verbose_name="Parentesco do Contato de Apoio")
    contato_apoio = models.CharField(null=True, blank=True, max_length=20, verbose_name="Telefone do Contato de Apoio")
    dat_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    vlr_sessao = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da Sessão")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        db_table = '"hamilton"."pacientes"'
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

class Terapeuta(models.Model):
    pk_terapeuta = models.AutoField(primary_key=True, verbose_name="ID")
    fk_decano = models.ForeignKey(
        Decano, 
        on_delete=models.CASCADE, 
        db_column='fk_decano',
        verbose_name="Decano"
    )
    fk_abordagem = models.ForeignKey(
        Abordagem,  # Usando a classe importada corretamente
        on_delete=models.CASCADE, 
        db_column='fk_abordagem',
        verbose_name="Abordagem"
    )
    fk_nucleo = models.ForeignKey(
        Nucleo,  # Usando a classe importada corretamente
        on_delete=models.CASCADE, 
        db_column='fk_nucleo',
        verbose_name="Núcleo"
    )
    fk_clinica = models.ForeignKey(
        Clinica,  # Usando a classe importada corretamente
        on_delete=models.CASCADE, 
        db_column='fk_clinica',
        verbose_name="Clínica"
    )
    fk_modalidade = models.ForeignKey(
        Modalidade,  # Usando a classe importada corretamente
        on_delete=models.CASCADE, 
        db_column='fk_modalidade',
        verbose_name="Modalidade"
    )
    nome = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone", help_text="Exemplo: 31988553344 Não coloque +55/espaços/parênteses")
    dat_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    sexo = models.CharField(
        max_length=1, 
        choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')],
        verbose_name="Sexo"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        ordering = ['nome']
        db_table = '"hamilton"."terapeutas"'
        verbose_name = "Terapeuta"
        verbose_name_plural = "Terapeutas"
    
    def __str__(self):
        return self.nome


class Consulta(models.Model):
    
    pk_consulta = models.AutoField(primary_key=True, verbose_name="ID")
    fk_decano = models.ForeignKey(
        Decano, 
        on_delete=models.CASCADE, 
        db_column='fk_decano',
        verbose_name="Decano"
    )
    fk_terapeuta = models.ForeignKey(
        Terapeuta, 
        on_delete=models.CASCADE, 
        db_column='fk_terapeuta',
        verbose_name="Terapeuta"
    )
    fk_paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE, 
        db_column='fk_paciente',
        verbose_name="Paciente"
    )
    vlr_consulta = models.IntegerField(verbose_name="Valor da Consulta")
    is_realizado = models.BooleanField(null=True, blank=True, verbose_name="Realizada")
    is_pago = models.BooleanField(null=True, blank=True, verbose_name="Paga")
    vlr_pago = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Valor Pago"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    data = models.DateField(null=True, blank=True, verbose_name="Data da Consulta")


    class Meta:
        db_table = '"hamilton"."consultas"'
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        constraints = [
            models.CheckConstraint(
                check=models.Q(vlr_pago__gte=0),
                name='check_vlr_pago_greater_equal_0'
            ),
        ]

    
    def __str__(self):
        return f"Consulta do {self.fk_paciente} pelo {self.fk_terapeuta}"
    
