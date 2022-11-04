from rest_framework import serializers

from .models import User, Location, Personel, DocCase, ImageCase, VideoCase
from .models import VideoMedia, ImageMedia, DocMedia
from .ModelSerializers.CaseSerializer import *
from .ModelSerializers.UserSerializer import *
