from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Paises)
class PaisesAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao')
    search_fields = ('codigo', 'descricao')
    list_filter = ('codigo', 'descricao')
    ordering = ('codigo', 'descricao')
    list_per_page = 10
    
@admin.register(Municipios)
class MunicipiosAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao')
    search_fields = ('codigo', 'descricao')
    list_filter = ('codigo', 'descricao')
    ordering = ('codigo', 'descricao')
    list_per_page = 10
    
@admin.register(Qualificacoes)
class QualificacoesAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao')
    search_fields = ('codigo', 'descricao')
    list_filter = ('codigo', 'descricao')
    ordering = ('codigo', 'descricao')
    list_per_page = 10
    
@admin.register(Naturezas)
class NaturezasAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao')
    search_fields = ('codigo', 'descricao')
    list_filter = ('codigo', 'descricao')
    ordering = ('codigo', 'descricao')
    list_per_page = 10
    
@admin.register(CNAEs)
class CNAEsAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao')
    search_fields = ('codigo', 'descricao')
    list_filter = ('codigo', 'descricao')
    ordering = ('codigo', 'descricao')
    list_per_page = 10
    
@admin.register(Estabelecimentos)
class EstabelecimentosAdmin(admin.ModelAdmin):
    list_display = ('cnpj_basico_id', 'nome_fantasia', 'municipio')
    # list_filter = ('cnpj', 'razao_social', 'nome_fantasia', 'situacao_cadastral', 'data_situacao_cadastral', 'motivo_situacao_cadastral', 'nome_cidade_exterior', 'codigo_natureza_juridica')
    # ordering = ('cnpj', 'razao_social', 'nome_fantasia', 'situacao_cadastral', 'data_situacao_cadastral', 'motivo_situacao_cadastral', 'nome_cidade_exterior', 'codigo_natureza_juridica')
    list_per_page = 10
    
# @admin.register(Empresas)
# class EmpresasAdmin(admin.ModelAdmin):
#     list_display = ('cnpj', 'razao_social', 'nome_fantasia', 'situacao_cadastral', 'data_situacao_cadastral', 'motivo_situacao_cadastral', 'nome_cidade_exterior', 'codigo_natureza_juridica', 'data_inicio_atividade', 'cnae_fiscal', 'tipo_logradouro', 'logradouro', 'numero', 'complemento', 'bairro', 'cep', 'uf', 'codigo_municipio', 'municipio', 'ddd_1', 'telefone_1', 'ddd_2', 'telefone_2', 'ddd_fax', 'fax', 'correio_eletronico', 'qualificacao_responsavel', 'capital_social', 'porte', 'opcao_pelo_simples', 'data_opcao_pelo_simples', 'data_exclusao_do_simples', 'opcao_pelo_mei', 'situacao_especial', 'data_situacao_especial')
#     search_fields = ('cnpj', 'razao_social', 'nome_fantasia', 'situacao_cadastral', 'data_situacao_cadastral', 'motivo_situacao_cadastral', 'nome_cidade_exterior', 'codigo_natureza_juridica', 'data_inicio_atividade', 'cnae_fiscal', 'tipo_logradouro', 'logradouro', 'numero', 'complemento', 'bairro', 'cep', 'uf', 'codigo_municipio', 'municipio', 'ddd_1', 'telefone_1', 'ddd_2', 'telefone_2', 'ddd_fax', 'fax', 'correio_eletronico', 'qualificacao_responsavel', 'capital_social', 'porte', 'opcao_pelo_simples', 'data_opcao_pelo_simples', 'data_exclusao_do_simples', 'opcao_pelo_mei', 'situacao_especial', 'data_situacao_especial')
    # list_filter = ('cnpj', 'razao_social', 'nome_fantasia', 'situacao_cadastral', 'data_situacao_cadastral', 'motivo_situacao_cadastral', 'nome_cidade_exterior', 'codigo_natureza_juridica')
    
@admin.register(Motivos)
class MotivosAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao')
    search_fields = ('codigo', 'descricao')
    list_filter = ('codigo', 'descricao')
    ordering = ('codigo', 'descricao')
    list_per_page = 10
    