from rest_framework import serializers
from ..models import AuthorityRequest, AccessRequest, AccessRequestComponent
from ..ModelSerializers.UserSerializer import UserSerializer
from ..ModelSerializers.CaseSerializer import ImageCaseSerializer, VideoCaseSerializer


class BaseRequestSerializer(serializers.ModelSerializer):
    request_form = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    title = serializers.CharField(max_length = 200)
    comments = serializers.CharField(max_length = 300)

class AuthorityRequestSerializer(BaseRequestSerializer):
    request_form1_requested_by = UserSerializer()

    auth_from = serializers.IntegerField()
    auth_to = serializers.IntegerField()
    status = serializers.IntegerField()

    class Meta:
        model = AuthorityRequest
        fields = (
            'request_form',
            'created_at',
            'title',
            'comments',
            'request_form1_requested_by',
            'auth_from',
            'auth_to',
            'status',
            'id'
        )

class AccessRequestComponentSerializer(serializers.ModelSerializer):
    requesting_case_form = serializers.IntegerField()
    
    image_case = ImageCaseSerializer()
    video_case = VideoCaseSerializer()
    doc_case = VideoCaseSerializer()

    status = serializers.IntegerField()

    class Meta:
        model = AccessRequestComponent
        fields = (
            'requesting_case_form',
            'image_case',
            'video_case',
            'doc_case',
            'status',
            'id'
        )


class AccessRequestSerializer(BaseRequestSerializer):
    request_form0_requested_by = UserSerializer()
    
    # This actually over-fetches Case data such as url, extension, attendee etc.
    # Implementation will be made in the future with 'PeekAccessComponentSerializer' class
    # that optimizes fetching data size fittingly to the access request browsing.

    request_components = AccessRequestComponentSerializer(many = True)
    status = serializers.IntegerField()

    class Meta:
        model = AccessRequest
        fields = (
            'request_form',
            'created_at',
            'title',
            'comments',
            'request_form0_requested_by',
            'request_components',
            'status',
            'id'
        )