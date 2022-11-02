from rest_framework import serializers
from ..models import User, Location, Personel, DocCase, ImageCase, VideoCase
from ..models import VideoMedia, ImageMedia, DocMedia


class ImageMediaSerializer(serializers.ModelSerializer):
    url = serializers.ImageField()

    class Meta:
        model = ImageMedia
        fields = (
            'url',
        )

class VideoMediaSerializer(serializers.ModelSerializer):
    url = serializers.FileField()

    class Meta:
        model = VideoMedia
        fields = (
            'url',
        )