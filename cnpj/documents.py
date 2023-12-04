import warnings

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch.exceptions import ElasticsearchWarning

from .models import Empresas

warnings.filterwarnings("ignore", category=ElasticsearchWarning)

#


@registry.register_document
class EmpresasDocument(Document):
    class Index:
        name = "empresas"
        settings = {"number_of_shards": 1, "number_of_replicas": 1}

    class Django:
        model = Empresas

        fields = [
            "razao_social_limpa",
        ]


#
