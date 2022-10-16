from . import abstractModels
from . import UserModel
#from . import OrganizationModel
from django.db import models



class Location(abstractModels.AbstractCase):
    case_form = 4
    construction_date = models.DateTimeField()
    #connected_office = models.ManyToManyField(OrganizationModel.Organization, related_name="part_of")


class Personel(abstractModels.AbstractCase):
    case_form = 3
    birth_date = models.DateTimeField()
    affiliation = models.ForeignKey(Location, on_delete=models.SET_NULL, null = True)
    prefix = models.CharField(max_length=20)
    connected_account = models.ForeignKey(UserModel.User, on_delete=models.SET_NULL, null = True)


class VideoCase(abstractModels.AbstractCase):

    case_form = 1
    associate = models.ForeignKey(UserModel.User, on_delete=models.SET_NULL, null = True)
    attendee = models.ManyToManyField(Personel, related_name = 'appears_in')
    location = models.ForeignKey(Location, on_delete = models.SET_NULL, null = True)
    produced = models.IntegerField()
    affiliation = models.ForeignKey(Location, on_delete=models.SET_NULL, null = True)
    
    class Meta: 
        abstract = False

class ImageCase(VideoCase):
    case_form = 0
    class Meta:
        abstract = False

class DocCase(abstractModels.AbstractCase):
    case_form = 2
    form = models.IntegerField()
    writer = models.ManyToManyField(Personel, related_name = 'wrote')
    referenced_personel = models.ManyToManyField(Personel, related_name = 'referenced_in')
    
    class Meta:
        abstract = False

