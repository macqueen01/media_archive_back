from django.db import models
from . import abstractModels
from . import CaseModel

class VideoMedia(abstractModels.AbstractVideoMedia):
    referenced_in = models.ManyToManyField(to = CaseModel.VideoCase, related_name = "include")
    profile_of = models.ManyToManyField(to = CaseModel.Personel, related_name = "profile")
    image_of = models.ManyToManyField(to = CaseModel.Location, related_name = "view")
    class Meta:
        abstract = False

class ImageMedia(abstractModels.AbstractImageMedia):
    referenced_in = models.ManyToManyField(to = CaseModel.ImageCase, related_name = "include")
    class Meta:
        abstract = False

class DocMedia(abstractModels.AbstractDocumentMedia):
    referenced_in = models.ManyToManyField(to = CaseModel.DocCase, related_name = "include")
    class Meta:
        abstract = False



