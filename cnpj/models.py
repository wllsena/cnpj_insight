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
)

RAZAO_SOCIAL_LENGTH = 150
SOCIO_LENGTH = 150
UF_LENGTH = 2
CPNJ_CPF_SOCIO_LENGTH = 14
REPRESENTANTE_LEGAL_LENGTH = 11

#


class Paises(Model):
    codigo = PositiveSmallIntegerField(primary_key=True)
    descricao = TextField()

    def __str__(self):
        return f"{self.codigo}"


class Municipios(Model):
    codigo = PositiveSmallIntegerField(primary_key=True)
    descricao = TextField()

    def __str__(self):
        return f"{self.codigo}"


class Qualificaoes(Model):
    codigo = PositiveSmallIntegerField(primary_key=True)
    descricao = TextField()

    def __str__(self):
        return f"{self.codigo}"


class Naturezas(Model):
    codigo = PositiveSmallIntegerField(primary_key=True)
    descricao = TextField()

    def __str__(self):
        return f"{self.codigo}"


class CNAEs(Model):
    codigo = PositiveIntegerField(primary_key=True)
    descricao = TextField()

    def __str__(self):
        return f"{self.codigo}"


class Motivos(Model):
    codigo = PositiveSmallIntegerField(primary_key=True)
    descricao = TextField()

    def __str__(self):
        return f"{self.codigo}"


class Empresas(Model):
    cnpj_basico = PositiveIntegerField(primary_key=True)
    razao_social = CharField(max_length=RAZAO_SOCIAL_LENGTH, db_index=True)
    natureza_juridica = ForeignKey(Naturezas, related_name="empresas", on_delete=PROTECT)
    qualificacao_resposavel = ForeignKey(Qualificaoes, related_name="empresas", on_delete=PROTECT)
    capital_social = FloatField()
    porte_empresa = PositiveSmallIntegerField(null=True, default=None)
    ente_federativo_responsavel = TextField(null=True, default=None)

    def __str__(self):
        return f"{self.cnpj_basico}"


class Estabelicimentos(Model):
    cnpj_basico_ordem = PositiveBigIntegerField(primary_key=True)
    cnpj_basico = ForeignKey(Empresas, related_name="estabelicimentos", on_delete=PROTECT)
    cnpj_ordem = PositiveSmallIntegerField()
    cnpj_dv = PositiveSmallIntegerField()
    matriz_filial = PositiveSmallIntegerField()
    nome_fantasia = TextField(null=True, default=None)
    situacao_cadastral = PositiveSmallIntegerField()
    data_situacao_cadastral = DateField()
    motivo_situacao_cadastral = ForeignKey(
        Motivos, related_name="estabelicimentos", on_delete=PROTECT
    )
    nome_cidade_exterior = TextField(null=True, default=None)
    pais = ForeignKey(
        Paises, null=True, default=None, related_name="estabelicimentos", on_delete=PROTECT
    )
    data_inicio_atividade = DateField()
    cnae_fiscal_principal = ForeignKey(CNAEs, related_name="estabelicimentos", on_delete=PROTECT)
    cnae_fiscal_secundaria = TextField(null=True, default=None)
    tipo_logradouro = TextField(null=True, default=None)
    logradouro = TextField(null=True, default=None)
    numero = TextField(null=True, default=None)
    complemento = TextField(null=True, default=None)
    bairro = TextField(null=True, default=None)
    cep = TextField(null=True, default=None)
    uf = CharField(max_length=UF_LENGTH)
    municipio = ForeignKey(Municipios, related_name="estabelicimentos", on_delete=PROTECT)
    ddd1 = TextField(null=True, default=None)
    telefone1 = TextField(null=True, default=None)
    ddd2 = TextField(null=True, default=None)
    telefone2 = TextField(null=True, default=None)
    ddd_fax = TextField(null=True, default=None)
    fax = TextField(null=True, default=None)
    correio_eletronico = TextField(null=True, default=None)
    situacao_especial = TextField(null=True, default=None)
    data_situacao_especial = DateField(null=True, default=None)
    obs = TextField(null=True, default=None)

    def __str__(self):
        return f"{self.cnpj_basico_ordem}"


class Simples(Model):
    cnpj_basico = ForeignKey(Empresas, related_name="simples", primary_key=True, on_delete=PROTECT)
    opcao_simples = BooleanField()
    data_opcao_simples = DateField()
    data_exclusao_simples = DateField()
    opcao_mei = BooleanField()
    data_opcao_mei = DateField()
    data_exclusao_mei = DateField()

    def __str__(self):
        return f"{self.cnpj_basico}"


class Socios(Model):
    cnpj_basico = ForeignKey(Empresas, related_name="socios", on_delete=PROTECT)
    identificador_socio = PositiveSmallIntegerField()
    nome_socio = CharField(max_length=SOCIO_LENGTH, null=True, default=None, db_index=True)
    cnpj_cpf_socio = CharField(max_length=CPNJ_CPF_SOCIO_LENGTH, null=True, default=None)
    qualificacao_socio = ForeignKey(Qualificaoes, related_name="socios", on_delete=PROTECT)
    data_entrada_sociedade = DateField()
    pais = ForeignKey(Paises, related_name="socios", null=True, default=None, on_delete=PROTECT)
    representante_legal = CharField(
        max_length=REPRESENTANTE_LEGAL_LENGTH,
    )
    nome_representante = TextField(null=True, default=None)
    qualificacao_representante_legal = ForeignKey(
        Qualificaoes,
        related_name="socios_representante",
        on_delete=PROTECT,
    )
    faixa_etaria = PositiveSmallIntegerField()

    class Meta:
        unique_together = [("cnpj_basico", "nome_socio")]

    def __str__(self):
        return f"{self.cnpj_basico}({self.nome_socio})"


#
