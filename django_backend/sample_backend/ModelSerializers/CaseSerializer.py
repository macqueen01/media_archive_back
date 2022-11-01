from rest_framework import serializers
from ..models import User, Location, Personel, DocCase, ImageCase, VideoCase
from ..models import VideoMedia, ImageMedia, DocMedia

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ImageMediaSerializer(serializers.ModelSerializer):
    url = serializers.ImageField()

    class Meta:
        model = ImageMedia
        fields = (
            'url',
        )

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

class BrowseCaseSerializer(serializers.ModelSerializer):
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
                   'include'
                )

class ImageUploadSerializer(serializers.ModelSerializer):
    form = serializers.IntegerField()
    title = serializers.CharField(max_length = 30)
    created_at = serializers.DateTimeField()
    content = serializers.CharField()
    private = serializers.IntegerField()
    produced = serializers.IntegerField()

    associate = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    location = serializers.PrimaryKeyRelatedField(queryset = Location.objects.all())
    attendee = serializers.PrimaryKeyRelatedField(queryset = Personel.objects.all(), many = True)
    affiliation = serializers.PrimaryKeyRelatedField(queryset = Location.objects.all())


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
                   'include'
                )


