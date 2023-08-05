from datetime import datetime

from elasticsearch_dsl import Search, Q
from flask_taxonomies.models import TaxonomyTerm
from invenio_search import current_search_client

from flask_taxonomies_es.serializer import get_taxonomy_term
from flask_taxonomies_es.utils import _get_taxonomy_slug_from_url


class TaxonomyESAPI:
    """
    Constructor takes Flask app as parameter. However, it is not necessary create class instance.
    Class instance should be called wit proxy method: current_flask_taxonomies_es.
    """

    def __init__(self, app):
        self.app = app
        self.index = app.config["TAXONOMY_ELASTICSEARCH_INDEX"]
        self._create_index()

    def _create_index(self):
        with self.app.app_context():
            if not current_search_client.indices.exists(self.index):
                current_search_client.indices.create(
                    index=self.index,
                    ignore=400,
                    body={}
                )

    def set(self, taxonomy_term: TaxonomyTerm, timestamp=datetime.utcnow()) -> None:
        """
        Save serialized taxonomy into Elasticsearch. It create new or update old taxonomy record.

        :param taxonomy_term: Taxonomy term class from flask-taxonomies
        :type taxonomy_term: TaxonomyTerm
        :param timestamp: Datetime class
        :type timestamp: Datetime class
        :return: None
        :rtype: None
        """
        if taxonomy_term.parent:
            body = get_taxonomy_term(
                code=taxonomy_term.taxonomy.slug,
                slug=taxonomy_term.slug,
                timestamp=timestamp
            )
            current_search_client.index(
                index=self.index,
                id=taxonomy_term.id,
                body=body
            )

    def remove(self, taxonomy_term: TaxonomyTerm = None, taxonomy_code: str = None,
               slug: str = None) -> None:
        """
        Remove taxonomy term from elasticsearch index. It takes either TaxonomyTerm class or
        taxonomy code with slug as strings.

        :param taxonomy_term: Taxonomy term class from flask-taxonomies
        :type taxonomy_term: TaxonomyTerm
        :param taxonomy_code: Code of taxonomy.
        :type taxonomy_code: str
        :param slug: Taxonomy slug as string
        :type slug: str
        :return: None
        :rtype: None
        """
        if taxonomy_term:
            id_ = taxonomy_term.id
        elif taxonomy_code and slug:
            id_ = self.get(taxonomy_code, slug)["id"]
        else:
            raise Exception("TaxonomyTerm or Taxonomy Code with slug must be specified")
        current_search_client.delete(
            index=self.index,
            id=id_
        )

    def get(self, taxonomy_code: str, slug: str):
        """
        Return serialized taxonomy term. Takes taxonomy code and slug as strings.

        :type taxonomy_code: str
        :param slug:
        :type slug: str
        :return: Serialized taxonomy term as dict
        :rtype: dict
        """
        s = Search(using=current_search_client, index=self.index)
        query = Q("match", taxonomy=taxonomy_code) & Q("match", slug=slug)
        results = list(s.query(query))
        if len(results) == 1:
            return results[0].to_dict()
        elif len(results) == 0:
            return None
        else:
            raise Exception(
                f'More than one taxonomy were found, slug \"{slug}\" and taxonomy \"'
                f'{taxonomy_code}\" should be unique.'
            )

    def get_ref(self, taxonomy_url: str):
        """
        Like the get method, it returns a serialized taxonomy. Instead of taxonomy and slug it
        takes the url as an argument.

        :param taxonomy_url: taxonomy term url, could be absolute or relative.
        :type taxonomy_url: str
        :return: Serialized taxonomy term as dict
        :rtype: dict
        """
        taxonomy, slug = _get_taxonomy_slug_from_url(taxonomy_url)
        return self.get(taxonomy, slug)

    def list(self, taxonomy_code: str) -> list:
        """
        Returns list of taxonomy terms. Individual records are serialized taxonomy terms.

        :param taxonomy_code: Code of taxonomy.
        :type taxonomy_code: str
        :return: List of serialized (dict) taxonomy terms
        :rtype: list
        """
        s = Search(using=current_search_client, index=self.index)
        query = Q("match", taxonomy=taxonomy_code)
        results = list(s.query(query))
        return [result.to_dict() for result in results]

    def reindex(self) -> None:
        """
        Reindex taxonomy index. Update taxonomy term and remove obsolete taxonomy terms.

        :return: None
        :rtype: None
        """
        timestamp = datetime.utcnow()
        self._synchronize_es(timestamp=timestamp)
        self._remove_old_es_term(timestamp)

    def _synchronize_es(self, timestamp=datetime.utcnow()) -> None:
        with self.app.app_context():
            for node in TaxonomyTerm.query.all():
                if timestamp:
                    self.set(node, timestamp=timestamp)
                else:
                    self.set(node)
                print(
                    f'Taxonomy term with slug: \"{node.slug}\" from taxonomy: \"'
                    f'{node.taxonomy.slug}\" has been updated')

    def _remove_old_es_term(self, timestamp) -> None:
        taxonomies = TaxonomyTerm.query.filter_by(level=1).all()
        for taxonomy in taxonomies:
            for node in self.list(taxonomy.slug):
                date_of_serialization = datetime.strptime(
                    node["date_of_serialization"],
                    '%Y-%m-%d %H:%M:%S.%f'
                )
                if date_of_serialization < timestamp:
                    self.remove(taxonomy_code=node["taxonomy"], slug=node["slug"])
                    print(
                        f'Taxonomy term with slug: \"{node.slug}\" from \"{node.taxonomy.slug}\" '
                        f'have been removed')
