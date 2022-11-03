from django.db import models
from . import UserModel
from . import CaseModel

import os


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

    class Meta:
        abstract = True


class AbstractMedia(models.Model):
    created_at = models.DateTimeField()
    name = models.CharField(max_length=300)
    extension = models.CharField(max_length = 20)

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





