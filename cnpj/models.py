from django.db.models import (
    PROTECT,
    BooleanField,
    CharField,
    DateField,
    FloatField,
    ForeignKey,
    Model,
    PositiveBigIntegerField,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    TextField,
    JSONField,
    OneToOneField,
    CASCADE
)
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

RAZAO_SOCIAL_LENGTH = 150
SOCIO_LENGTH = 150
UF_LENGTH = 2
CPNJ_CPF_SOCIO_LENGTH = 14
REPRESENTANTE_LEGAL_LENGTH = 11

#


class Paises(Model):
    codigo = PositiveSmallIntegerField(primary_key=True)
    descricao = TextField(null=True, default=None)

    def __str__(self):
        return f"{self.codigo}"


class Municipios(Model):
    codigo = PositiveSmallIntegerField(primary_key=True)
    descricao = TextField(null=True, default=None)

    def __str__(self):
        return f"{self.codigo}"


class Qualificacoes(Model):
    codigo = PositiveSmallIntegerField(primary_key=True)
    descricao = TextField(null=True, default=None)

    def __str__(self):
        return f"{self.codigo}"


class Naturezas(Model):
    codigo = PositiveSmallIntegerField(primary_key=True)
    descricao = TextField(null=True, default=None)

    def __str__(self):
        return f"{self.codigo}"


class CNAEs(Model):
    codigo = PositiveIntegerField(primary_key=True)
    descricao = TextField(null=True, default=None)

    def __str__(self):
        return f"{self.codigo}"


class Motivos(Model):
    codigo = PositiveSmallIntegerField(primary_key=True)
    descricao = TextField(null=True, default=None)

    def __str__(self):
        return f"{self.codigo}"


class Empresas(Model):
    cnpj_basico = PositiveIntegerField(primary_key=True)
    razao_social = CharField(max_length=RAZAO_SOCIAL_LENGTH, null=True, default=None, db_index=True)
    natureza_juridica = ForeignKey(Naturezas, related_name="empresas", on_delete=PROTECT)
    qualificacao_resposavel = ForeignKey(Qualificacoes, related_name="empresas", on_delete=PROTECT)
    capital_social = FloatField()
    porte_empresa = PositiveSmallIntegerField(null=True, default=None)
    ente_federativo_responsavel = TextField(null=True, default=None)
    razao_social_limpa = TextField(
        max_length=RAZAO_SOCIAL_LENGTH, null=True, default=None, db_index=True
    )

    def __str__(self):
        return f"{self.cnpj_basico}"


class Estabelecimentos(Model):
    cnpj_basico_id = PositiveBigIntegerField(primary_key=True)
    # cnpj_basico = ForeignKey(Empresas, related_name="estabelecimentos", on_delete=PROTECT)
    cnpj_ordem = PositiveSmallIntegerField()
    cnpj_dv = PositiveSmallIntegerField()
    matriz_filial = PositiveSmallIntegerField()
    nome_fantasia = TextField(null=True, default=None)
    situacao_cadastral = PositiveSmallIntegerField()
    # data_situacao_cadastral = DateField(null=True, default=None)
    motivo_situacao_cadastral = ForeignKey(
        Motivos, related_name="estabelecimentos", on_delete=PROTECT
    )
    nome_cidade_exterior = TextField(null=True, default=None)
    pais = ForeignKey(
        Paises, null=True, default=None, related_name="estabelecimentos", on_delete=PROTECT
    )
    # data_inicio_atividade = DateField(null=True, default=None)
    cnae_fiscal_principal = ForeignKey(CNAEs, related_name="estabelecimentos", on_delete=PROTECT)
    cnae_fiscal_secundaria = TextField(null=True, default=None)
    tipo_logradouro = TextField(null=True, default=None)
    logradouro = TextField(null=True, default=None)
    numero = TextField(null=True, default=None)
    complemento = TextField(null=True, default=None)
    bairro = TextField(null=True, default=None)
    cep = TextField(null=True, default=None)
    uf = CharField(max_length=UF_LENGTH)
    municipio = ForeignKey(Municipios, related_name="estabelecimentos", on_delete=PROTECT)
    ddd1 = TextField(null=True, default=None)
    telefone1 = TextField(null=True, default=None)
    ddd2 = TextField(null=True, default=None)
    telefone2 = TextField(null=True, default=None)
    ddd_fax = TextField(null=True, default=None)
    fax = TextField(null=True, default=None)
    correio_eletronico = TextField(null=True, default=None)
    situacao_especial = TextField(null=True, default=None)
    # data_situacao_especial = DateField(null=True, default=None)
    # obs = TextField(null=True, default=None)

    def __str__(self):
        return f"{self.cnpj_basico_id}"


class Simples(Model):
    cnpj_basico = ForeignKey(Empresas, related_name="simples", primary_key=True, on_delete=PROTECT)
    opcao_simples = BooleanField()
    data_opcao_simples = DateField(null=True, default=None)
    data_exclusao_simples = DateField(null=True, default=None)
    opcao_mei = BooleanField()
    data_opcao_mei = DateField(null=True, default=None)
    data_exclusao_mei = DateField(null=True, default=None)

    def __str__(self):
        return f"{self.cnpj_basico}"


class Socios(Model):
    cnpj_basico = ForeignKey(Empresas, related_name="socios", on_delete=PROTECT)
    identificador_socio = PositiveSmallIntegerField()
    nome_socio = CharField(max_length=SOCIO_LENGTH, null=True, default=None, db_index=True)
    cnpj_cpf_socio = CharField(max_length=CPNJ_CPF_SOCIO_LENGTH, null=True, default=None)
    qualificacao_socio = ForeignKey(Qualificacoes, related_name="socios", on_delete=PROTECT)
    data_entrada_sociedade = DateField()
    pais = ForeignKey(Paises, null=True, default=None, related_name="socios", on_delete=PROTECT)
    representante_legal = CharField(max_length=REPRESENTANTE_LEGAL_LENGTH, null=True, default=None)
    nome_representante = TextField(null=True, default=None)
    qualificacao_representante_legal = ForeignKey(
        Qualificacoes,
        related_name="socios_representante",
        on_delete=PROTECT,
    )
    faixa_etaria = PositiveSmallIntegerField()

    class Meta:
        unique_together = [("cnpj_basico", "nome_socio")]
        verbose_name = "Sócio"
        verbose_name_plural = "Sócios"

    def __str__(self):
        return f"{self.cnpj_basico}({self.nome_socio})"

class Account(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    # search history with list of empresas
    search_history = JSONField(null=True, default=list())
    # favorite list with list of empresas
    favorite_list = JSONField(null=True, default=list())
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        
@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
