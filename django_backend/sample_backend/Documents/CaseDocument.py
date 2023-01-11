from sample_backend.models import *
from elasticsearch_dsl import analyzer, tokenizer
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import fields, Document

nori_analyzer = analyzer('nori_analyzer',
    tokenizer=tokenizer('nori_tokenizer')
)


@registry.register_document
class PersonelDocument(Document):
    affiliation = fields.NestedField(properties={
        'title': fields.TextField(analyzer=nori_analyzer),
        'content': fields.TextField(analyzer=nori_analyzer)
    })
    prefix = fields.TextField(required=False, analyzer=nori_analyzer)
    connected_account = fields.NestedField(properties={
        'name': fields.TextField(analyzer=nori_analyzer),
        'position': fields.TextField(analyzer=nori_analyzer),
        'standing': fields.TextField(analyzer=nori_analyzer),
        'affiliation': fields.TextField(analyzer=nori_analyzer)
    }, required=False)

    title = fields.TextField(analyzer='nori_analyzer')
    content = fields.TextField(analyzer='nori_analyzer')

    class Index:
        name = 'personels'
        settings = {
            'number_of_shards': 5,
            'number_of_replicas': 0
        }

    class Django:
        model = Personel
        fields = [
            'created_at',
            'birth_date'
        ]
        related_models = [Location, User]

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, Location):
            return related_instance.personel_set.all()
        elif isinstance(related_instance, User):
            return related_instance.personel_set.all()
        



@registry.register_document
class LocationDocument(Document):
    
    #title = fields.TextField(analyzer='nori_analyzer')
    #content = fields.TextField(analyzer='nori_analyzer')
    
    class Index:
        name = 'location'
        settings = {
            'number_of_shards': 5,
            'number_of_replicas': 0
        }

    class Django:
        model = Location
        fields = [
            'created_at'
        ]




@registry.register_document
class VideoCaseIndex(Document):
    associate = fields.NestedField(properties={
        'title': fields.TextField(analyzer=nori_analyzer)
    }, required=False)
    attendee = fields.NestedField(properties={
        'title': fields.TextField(analyzer=nori_analyzer)
    }, required=False)
    location = fields.NestedField(properties={
        'title': fields.TextField(analyzer=nori_analyzer)
    }, required=False)
    affiliation = fields.NestedField(properties={
        'title': fields.TextField(analyzer=nori_analyzer)
    }, required=False)

    title = fields.TextField(analyzer='nori_analyzer')
    content = fields.TextField(analyzer='nori_analyzer')

    class Index:
        name = 'video_cases'
        settings = {
            'number_of_shards': 3,
            'number_of_replicas': 0
        }


    class Django:
        model = VideoCase
        fields = [
            'created_at',
            'produced'
        ]
        related_models = [Personel, Location]

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, Location):
            return related_instance.to_location_in_form1.all()
        elif isinstance(related_instance, User):
            return related_instance.appears_in_form1.all()

@registry.register_document   
class ImageCaseIndex(Document):
    associate = fields.NestedField(properties={
        'title': fields.TextField(analyzer=nori_analyzer)
    }, required=False)
    attendee = fields.NestedField(properties={
        'title': fields.TextField(analyzer=nori_analyzer)
    }, required=False)
    location = fields.NestedField(properties={
        'title': fields.TextField(analyzer=nori_analyzer)
    }, required=False)
    affiliation = fields.NestedField(properties={
        'title': fields.TextField(analyzer=nori_analyzer)
    }, required=False)

    title = fields.TextField(analyzer='nori_analyzer')
    content = fields.TextField(analyzer='nori_analyzer')


    class Index:
        name = 'image_cases'
        settings = {
            'number_of_shards': 5,
            'number_of_replicas': 0
        }


    class Django:
        model = ImageCase
        fields = [
            'created_at',
            'produced'
        ]
        related_models = [Location, Personel]
    
    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, Location):
            return related_instance.to_location_in_form0.all()
        elif isinstance(related_instance, User):
            return related_instance.appears_in_form0.all()


@registry.register_document
class DocCaseIndex(Document):
    writer = fields.NestedField(properties={
        'title': fields.TextField(analyzer=nori_analyzer)
    })
    referenced_personel = fields.NestedField(properties={
        'title': fields.TextField(analyzer=nori_analyzer)
    })

    title = fields.TextField(analyzer='nori_analyzer')
    content = fields.TextField(analyzer='nori_analyzer')

    class Index:
        name='doc_cases'
        settings = {
            'number_of_shards': 5,
            'number_of_replicas': 0
        }

    class Django:
        model = DocCase
        fields = [
            'created_at'
        ]
        related_models = [Location, Personel]
    

