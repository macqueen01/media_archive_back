from django.db import models
from . import UserModel
from . import CaseModel

import os

class CaseManager(models.Manager):

    def grant_permission_to(self, case, user, status):
        # this gets users with current permission
        if status == 1:
            exec(f"case.form{case.form}_accessed_by.add(user)")
            case.save()
            return False
        else:
            return True
        
    def get_permitted_users(self, case):
        case_form = case.form
        if case_form == 0:
            return case.form.form0_accessed_by
        elif case_form == 1:
            return case.form.form1_accessed_by
        elif case_form == 2:
            return case.form.form2_accessed_by
        else: 
            return False

class RequestManager(models.Manager):

    def get_subject(self, request):
        if request.is_authority == 0: 
            return request.request_form0_requested_by
        elif request.is_authority == 1:
            return request.request_form1_requested_by
        return None
    




class AbstractCase(models.Model):
    # form : 
    #   if form == 0 --> photo
    #   if form == 1 --> video
    #   if form == 2 --> document
    #   if form == 3 --> personel
    #   if form == 4 --> location
    case_form = None
    
    # Field functions dependent on case_form
    accessed_by = lambda form: f"form{form}_accessed_by = models.ManyToManyField(to = UserModel.User, related_name = 'access_to_form{form}')"
    form = lambda form: f"form = models.IntegerField(default={form})"

    title = models.CharField(max_length = 30)
    created_at = models.DateTimeField()
    content = models.TextField()
    private = models.IntegerField()

    objects = CaseManager()

    class Meta:
        abstract = True


class AbstractMedia(models.Model):
    created_at = models.DateTimeField()
    name = models.CharField(max_length=300)
    extension = models.CharField(max_length = 20)

    class Meta:
        abstract = True

class AbstractRequest(models.Model):
    is_authority = None

    # request form is assigned to either 0 (access request) or 1 (authority request)

    requested_by = lambda is_authority: f"request_form{is_authority}_requested_by = models.ForeignKey(to = UserModel.User, on_delete = models.CASCADE, related_name = 'requested_form{is_authority}')"
    form = lambda is_authority: f"request_form = models.IntegerField(default={is_authority})"

    created_at = models.DateTimeField()
    title = models.CharField(max_length = 200)
    comments = models.CharField(max_length = 300)

    objects = RequestManager()
    
    class Meta:
        abstract = True


# Abstract Child Classes


class AbstractVideoMedia(AbstractMedia):
    archive = models.FileField(upload_to = 'stream/video/%Y%m%d', blank = True)
    url = models.CharField(max_length = 300, blank = True)
    thumbnail = models.CharField(max_length = 500, blank = True)

    def filename(self):
        basename = os.path.basename(self.file.name)
        return os.path.splitext(basename)[0]

    class Meta:
        abstract = True

class AbstractImageMedia(AbstractMedia):
    url = models.ImageField(upload_to = 'stream/image/%Y%m%d')
    

    def filename(self):
        basename = os.path.basename(self.file.name)
        return os.path.splitext(basename)

    class Meta:
        abstract = True

class AbstractDocumentMedia(AbstractMedia):
    url = models.FileField(upload_to = 'stream/document/%Y%m%d')
    thumbnail = models.CharField(max_length = 500, blank = True)

    def filename(self):
        basename = os.path.basename(self.file.name)
        return os.path.splitext(basename)[0]

    class Meta:
        abstract = True





