from sample_backend.models import *
from .UserDocument import UserInnerDoc
from elasticsearch_dsl import Document, analyzer, InnerDoc, Keyword, Date, Integer, Nested, Text
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import fields

nori_analyzer = analyzer('nori_analyzer',
    tokenizer='nori_tokenizer'
)


class LocationInnerDoc(InnerDoc):
    construction_date = fields.DateField()
    #connected_office = Nested(OrganizationInnerDoc)

    title = fields.TextField(analyzer='nori_analyzer')
    content = fields.TextField(analyzer='nori_analyzer')
    created_at = fields.DateField()

location_inner_doc_properties = {
    'construction_date': fields.DateField(),
    'title': fields.TextField(analyzer='nori_analyzer'),
    'content': fields.TextField(analyzer='nori_analyzer'),
    'created_at': fields.DateField(),
}


class PersonelInnerDoc(InnerDoc):
    birth_date = fields.DateField(required=False)
    affiliation = fields.Nested(properties=location_inner_doc_properties, required=False)
    prefix = fields.KeywordField(required=False)
    connected_account = fields.Nested(UserInnerDoc, required=False)

    title = fields.TextField(analyzer='nori_analyzer')
    content = fields.TextField(analyzer='nori_analyzer')
    created_at = fields.DateField()

personel_inner_doc_properties = {
    'birth_date': PersonelInnerDoc().birth_date,
    'affiliation': PersonelInnerDoc().affiliation,
    'prefix': PersonelInnerDoc().prefix,
    'connected_account': PersonelInnerDoc().connected_account,
    'title': PersonelInnerDoc().title,
    'content': PersonelInnerDoc().content,
    'created_at': PersonelInnerDoc().created_at
}

@registry.register_document
class PersonelDocument(Document):
    personel = fields.Nested(properties=personel_inner_doc_properties)

    class Django:
        model = Personel
        fields = [
            'birth_date',
            'title',
            'prefix',
            'content',
            'connected_account',
            'created_at'
        ]
        index = 'personels'









@registry.register_document
class LocationDocument(Document):
    location = Nested(LocationInnerDoc)

    class Django:
        model = Location
        fields = [
            'title',
            'affiliation',
            'content',
            'created_at'
        ]
        index = 'locations'

@registry.register_document
class VideoCaseIndex(Document):
    associate = Nested(PersonelInnerDoc, required=False)
    attendee = Nested(PersonelInnerDoc, required=False)
    location = Nested(LocationInnerDoc, required=False)
    affiliation = Nested(LocationInnerDoc, required=False)
    produced = Integer()

    title = Text(analyzer='nori_analyzer')
    content = Text(analyzer='nori_analyzer')
    created_at = Date()

    class Django:
        model = VideoCase
        fields = [
            'associate',
            'attendee',
            'location',
            'affiliation'
            'created_at',
            'title',
            'content'
        ]
        index = 'video_cases'

@registry.register_document   
class ImageCaseIndex(Document):
    associate = Nested(PersonelInnerDoc, required=False)
    attendee = Nested(PersonelInnerDoc, required=False)
    location = Nested(LocationInnerDoc, required=False)
    affiliation = Nested(LocationInnerDoc, required=False)
    produced = Integer()

    title = Text(analyzer='nori_analyzer')
    content = Text(analyzer='nori_analyzer')
    created_at = Date()

    class Django:
        model = ImageCase
        fields = [
            'associate',
            'attendee',
            'location',
            'affiliation'
            'created_at',
            'title',
            'content'
        ]
        index = 'image_cases'

@registry.register_document
class DocCaseIndex(Document):
    writer = Nested(PersonelInnerDoc, required = False)
    referenced_personel = Nested(PersonelInnerDoc, required=False)

    title = Text(analyzer='nori_analyzer')
    content = Text(analyzer='nori_analyzer')
    created_at = Date()

    class Django:
        model = DocCase
        fields = [
            'id',
            'created_at',
            'title',
            'content',
            'writer',
            'referenced_personel'
        ]
        index = 'document_cases'