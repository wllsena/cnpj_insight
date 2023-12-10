from typing import List
import warnings
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch.exceptions import ElasticsearchWarning
from .models import Empresas

warnings.filterwarnings("ignore", category=ElasticsearchWarning)


@registry.register_document
class EmpresasDocument(Document):
    """Document class for Empresas model.

    This class represents a document that will be stored in Elasticsearch.
    It includes the index name and settings, and the fields that will be
    included in the document.
    """

    class Index:
        """Index class for EmpresasDocument.

        This class includes the name of the index in Elasticsearch and its settings.
        """

        name: str = "empresas"
        settings: dict = {"number_of_shards": 1, "number_of_replicas": 1}

    class Django:
        """Django class for EmpresasDocument.

        This class includes the model that the document represents and the fields
        that will be included in the document.
        """

        model: type = Empresas
        fields: List[str] = ["razao_social_limpa"]