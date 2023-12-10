from typing import Tuple, Type
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db.models import Model
from .models import (
    Paises, Municipios, Qualificacoes,
    Naturezas, CNAEs, Estabelecimentos,
    Motivos, Account
)


@admin.register(Paises)
class PaisesAdmin(admin.ModelAdmin):
    """Admin interface for Paises model."""

    list_display: Tuple[str, str] = ('codigo', 'descricao')
    search_fields: Tuple[str, str] = ('codigo', 'descricao')
    list_filter: Tuple[str, str] = ('codigo', 'descricao')
    ordering: Tuple[str, str] = ('codigo', 'descricao')
    list_per_page: int = 10


@admin.register(Municipios)
class MunicipiosAdmin(admin.ModelAdmin):
    """Admin interface for Municipios model."""

    list_display: Tuple[str, str] = ('codigo', 'descricao')
    search_fields: Tuple[str, str] = ('codigo', 'descricao')
    list_filter: Tuple[str, str] = ('codigo', 'descricao')
    ordering: Tuple[str, str] = ('codigo', 'descricao')
    list_per_page: int = 10


@admin.register(Qualificacoes)
class QualificacoesAdmin(admin.ModelAdmin):
    """Admin interface for Qualificacoes model."""

    list_display: Tuple[str, str] = ('codigo', 'descricao')
    search_fields: Tuple[str, str] = ('codigo', 'descricao')
    list_filter: Tuple[str, str] = ('codigo', 'descricao')
    ordering: Tuple[str, str] = ('codigo', 'descricao')
    list_per_page: int = 10


@admin.register(Naturezas)
class NaturezasAdmin(admin.ModelAdmin):
    """Admin interface for Naturezas model."""

    list_display: Tuple[str, str] = ('codigo', 'descricao')
    search_fields: Tuple[str, str] = ('codigo', 'descricao')
    list_filter: Tuple[str, str] = ('codigo', 'descricao')
    ordering: Tuple[str, str] = ('codigo', 'descricao')
    list_per_page: int = 10


@admin.register(CNAEs)
class CNAEsAdmin(admin.ModelAdmin):
    """Admin interface for CNAEs model."""

    list_display: Tuple[str, str] = ('codigo', 'descricao')
    search_fields: Tuple[str, str] = ('codigo', 'descricao')
    list_filter: Tuple[str, str] = ('codigo', 'descricao')
    ordering: Tuple[str, str] = ('codigo', 'descricao')
    list_per_page: int = 10


@admin.register(Estabelecimentos)
class EstabelecimentosAdmin(admin.ModelAdmin):
    """Admin interface for Estabelecimentos model."""

    list_display: Tuple[str, str, str] = ('cnpj_basico_id', 'nome_fantasia',
                                          'municipio')
    list_per_page: int = 10


@admin.register(Motivos)
class MotivosAdmin(admin.ModelAdmin):
    """Admin interface for Motivos model."""

    list_display: Tuple[str, str] = ('codigo', 'descricao')
    search_fields: Tuple[str, str] = ('codigo', 'descricao')
    list_filter: Tuple[str, str] = ('codigo', 'descricao')
    ordering: Tuple[str, str] = ('codigo', 'descricao')
    list_per_page: int = 10


class AccountInline(admin.StackedInline):
    """Admin interface for Account model."""

    model: Type[Model] = Account
    can_delete: bool = False
    verbose_name_plural: str = 'Contas'


class CustomizedUserAdmin(UserAdmin):
    """Admin interface for User model with Account inline."""

    inlines: Tuple[Type[AccountInline], ...] = (AccountInline, )


admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
