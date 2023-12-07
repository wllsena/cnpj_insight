# Generated by Django 4.1 on 2023-12-07 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CNAEs",
            fields=[
                ("codigo", models.PositiveIntegerField(primary_key=True, serialize=False)),
                ("descricao", models.TextField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Empresas",
            fields=[
                ("cnpj_basico", models.PositiveIntegerField(primary_key=True, serialize=False)),
                (
                    "razao_social",
                    models.CharField(db_index=True, default=None, max_length=150, null=True),
                ),
                ("capital_social", models.FloatField()),
                ("porte_empresa", models.PositiveSmallIntegerField(default=None, null=True)),
                ("ente_federativo_responsavel", models.TextField(default=None, null=True)),
                (
                    "razao_social_limpa",
                    models.TextField(db_index=True, default=None, max_length=150, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Motivos",
            fields=[
                ("codigo", models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ("descricao", models.TextField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Municipios",
            fields=[
                ("codigo", models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ("descricao", models.TextField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Naturezas",
            fields=[
                ("codigo", models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ("descricao", models.TextField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Paises",
            fields=[
                ("codigo", models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ("descricao", models.TextField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Qualificacoes",
            fields=[
                ("codigo", models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ("descricao", models.TextField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Simples",
            fields=[
                (
                    "cnpj_basico",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        primary_key=True,
                        related_name="simples",
                        serialize=False,
                        to="cnpj.empresas",
                    ),
                ),
                ("opcao_simples", models.BooleanField()),
                ("data_opcao_simples", models.DateField(default=None, null=True)),
                ("data_exclusao_simples", models.DateField(default=None, null=True)),
                ("opcao_mei", models.BooleanField()),
                ("data_opcao_mei", models.DateField(default=None, null=True)),
                ("data_exclusao_mei", models.DateField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Estabelecimentos",
            fields=[
                (
                    "cnpj_basico_ordem",
                    models.PositiveBigIntegerField(primary_key=True, serialize=False),
                ),
                ("cnpj_ordem", models.PositiveSmallIntegerField()),
                ("cnpj_dv", models.PositiveSmallIntegerField()),
                ("matriz_filial", models.PositiveSmallIntegerField()),
                ("nome_fantasia", models.TextField(default=None, null=True)),
                ("situacao_cadastral", models.PositiveSmallIntegerField()),
                ("data_situacao_cadastral", models.DateField(default=None, null=True)),
                ("nome_cidade_exterior", models.TextField(default=None, null=True)),
                ("data_inicio_atividade", models.DateField(default=None, null=True)),
                ("cnae_fiscal_secundaria", models.TextField(default=None, null=True)),
                ("tipo_logradouro", models.TextField(default=None, null=True)),
                ("logradouro", models.TextField(default=None, null=True)),
                ("numero", models.TextField(default=None, null=True)),
                ("complemento", models.TextField(default=None, null=True)),
                ("bairro", models.TextField(default=None, null=True)),
                ("cep", models.TextField(default=None, null=True)),
                ("uf", models.CharField(max_length=2)),
                ("ddd1", models.TextField(default=None, null=True)),
                ("telefone1", models.TextField(default=None, null=True)),
                ("ddd2", models.TextField(default=None, null=True)),
                ("telefone2", models.TextField(default=None, null=True)),
                ("ddd_fax", models.TextField(default=None, null=True)),
                ("fax", models.TextField(default=None, null=True)),
                ("correio_eletronico", models.TextField(default=None, null=True)),
                ("situacao_especial", models.TextField(default=None, null=True)),
                ("data_situacao_especial", models.DateField(default=None, null=True)),
                ("obs", models.TextField(default=None, null=True)),
                (
                    "cnae_fiscal_principal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="estabelicimentos",
                        to="cnpj.cnaes",
                    ),
                ),
                (
                    "cnpj_basico",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="estabelicimentos",
                        to="cnpj.empresas",
                    ),
                ),
                (
                    "motivo_situacao_cadastral",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="estabelicimentos",
                        to="cnpj.motivos",
                    ),
                ),
                (
                    "municipio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="estabelicimentos",
                        to="cnpj.municipios",
                    ),
                ),
                (
                    "pais",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="estabelicimentos",
                        to="cnpj.paises",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="empresas",
            name="natureza_juridica",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="empresas",
                to="cnpj.naturezas",
            ),
        ),
        migrations.AddField(
            model_name="empresas",
            name="qualificacao_resposavel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="empresas",
                to="cnpj.qualificacoes",
            ),
        ),
        migrations.CreateModel(
            name="Socios",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("identificador_socio", models.PositiveSmallIntegerField()),
                (
                    "nome_socio",
                    models.CharField(db_index=True, default=None, max_length=150, null=True),
                ),
                ("cnpj_cpf_socio", models.CharField(default=None, max_length=14, null=True)),
                ("data_entrada_sociedade", models.DateField()),
                ("representante_legal", models.CharField(default=None, max_length=11, null=True)),
                ("nome_representante", models.TextField(default=None, null=True)),
                ("faixa_etaria", models.PositiveSmallIntegerField()),
                (
                    "cnpj_basico",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="socios",
                        to="cnpj.empresas",
                    ),
                ),
                (
                    "pais",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="socios",
                        to="cnpj.paises",
                    ),
                ),
                (
                    "qualificacao_representante_legal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="socios_representante",
                        to="cnpj.qualificacoes",
                    ),
                ),
                (
                    "qualificacao_socio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="socios",
                        to="cnpj.qualificacoes",
                    ),
                ),
            ],
            options={
                "unique_together": {("cnpj_basico", "nome_socio")},
            },
        ),
    ]
