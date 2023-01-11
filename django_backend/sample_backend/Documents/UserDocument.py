from sample_backend.models import *
from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import analyzer, tokenizer, Search
from django_elasticsearch_dsl.registries import registry
from sample_backend import client


nori_analyzer = analyzer('nori_analyzer',
    tokenizer=tokenizer('nori_tokenizer')
)

@registry.register_document
class UserDocument(Document):
    name = fields.TextField(analyzer = nori_analyzer)
    position = fields.TextField(analyzer = nori_analyzer)
    standing = fields.TextField(analyzer = nori_analyzer)
    affiliation = fields.TextField(analyzer = nori_analyzer)

    class Index:
        name = 'users'
        settings = {
            'number_of_shards': 5,
            'number_of_replicas': 0
        }
    
    class Django:
        model = User
        fields = [
            'username'
        ]

'''
def index_new_users():
    # Get all users from the database
    users = User.objects.all()

    # Create a list of UserDocument instances
    docs = []
    for user in users:
        doc = UserDocument(
            meta={'id': user.pk},
            username=user.username,
            name=user.name,
            position=user.position,
            standing=user.standing,
            client_ip=user.client_ip,
            affiliation=user.affiliation
        )
        docs.append(doc)
    
    # Index the documents using the bulk method
    UserDocument.bulk(docs)

def index_user(user):

    # Indexing a model instance
    obj_index = UserDocument(
        meta={'id': user.pk},
        username=user.username,
        name=user.name,
        position=user.position,
        standing=user.standing,
        client_ip=user.client_ip,
        affiliation=user.affiliation
    )
    obj_index.save(using=client)

    return user.id

'''
def search_users(query):
    s = Search(using=client, index='users')
    s = s.query('multi_match', query=query, fields=['username', 'name', 'position', 'standing', 'client_ip', 'affiliation'], fuzziness=2)
    response = s.execute()
    return response

