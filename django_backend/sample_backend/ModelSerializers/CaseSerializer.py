from rest_framework import serializers
from ..models import User, Location, Personel, DocCase, ImageCase, VideoCase
from .MediaSerializer import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PersonelSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length = 30)
    
    class Meta:
        model = Personel
        fields = (
            'id',
            'title'
        )

class LocationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length = 30)

    class Meta:
        model = Location
        fields = (
            'id',
            'title'
        )


class BaseCaseSerializer(serializers.ModelSerializer):
    form = serializers.IntegerField()
    title = serializers.CharField(max_length = 30)
    created_at = serializers.DateTimeField()
    content = serializers.CharField()
    private = serializers.IntegerField()
    produced = serializers.IntegerField()

    associate = PersonelSerializer()
    location = LocationSerializer()
    attendee = PersonelSerializer(many = True)
    affiliation = LocationSerializer()


class ImageCaseSerializer(BaseCaseSerializer):
    include = ImageMediaSerializer(many = True)

    class Meta:
        model = ImageCase
        fields = ( 
                   'form',
                   'title',
                   'created_at',
                   'content',
                   'private',
                   'produced',
                   'associate',
                   'location',
                   'attendee',
                   'affiliation',
                   'include',
                   'id'
                )

class VideoCaseSerializer(BaseCaseSerializer):
    include = VideoMediaSerializer(many = True)

    class Meta:
        model = VideoCase
        fields = (
            'form',
            'title',
            'created_at',
            'content',
            'private',
            'produced',
            'associate',
            'location',
            'attendee',
            'affiliation',
            'include',
            'id'
        )

