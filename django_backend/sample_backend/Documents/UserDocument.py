from sample_backend.models import *
from elasticsearch_dsl import Document, Text, analyzer, Search, InnerDoc, Keyword, Nested
from django_elasticsearch_dsl.registries import registry
from sample_backend import client

nori_analyzer = analyzer('nori_analyzer',
    tokenizer='nori_tokenizer'
)

class UserInnerDoc(InnerDoc):
    username = Text(analyzer=nori_analyzer)
    name = Text(analyzer=nori_analyzer)
    position = Text(analyzer=nori_analyzer)
    standing = Text(analyzer=nori_analyzer)
    client_ip = Text()
    affiliation = Text(analyzer=nori_analyzer)


@registry.register_document
class UserDocument(Document):
    user = Nested(UserInnerDoc)
    
    class Django:
        model = User
        field = [
            'username',
            'name',
            'position',
            'standing',
            'affiliation'
        ]
        index = 'users'



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


def search_users(query):
    s = Search(using=client, index='users')
    s = s.query('multi_match', query=query, fields=['username', 'name', 'position', 'standing', 'client_ip', 'affiliation'], fuzziness=2)
    response = s.execute()
    return response

