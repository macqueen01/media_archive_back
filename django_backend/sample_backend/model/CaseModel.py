from . import abstractModels
from . import UserModel
#from . import OrganizationModel
from django.db import models



class Location(abstractModels.AbstractCase):
    case_form = 4
    form = abstractModels.AbstractCase.form(case_form)
    abstractModels.AbstractCase.accessed_by(case_form)

    construction_date = models.DateTimeField()
    #connected_office = models.ManyToManyField(OrganizationModel.Organization, related_name="part_of")


class Personel(abstractModels.AbstractCase):
    case_form = 3
    form = abstractModels.AbstractCase.form(case_form)
    abstractModels.AbstractCase.accessed_by(case_form)

    birth_date = models.DateTimeField()
    affiliation = models.ForeignKey(Location, on_delete=models.SET_NULL, null = True)
    prefix = models.CharField(max_length=20)
    connected_account = models.ForeignKey(UserModel.User, on_delete=models.SET_NULL, null = True)


class VideoCase(abstractModels.AbstractCase):

    case_form = 1
    form = abstractModels.AbstractCase.form(case_form)
    abstractModels.AbstractCase.accessed_by(case_form)

    associate = models.ForeignKey(UserModel.User, on_delete=models.SET_NULL, null = True)
    attendee = models.ManyToManyField(Personel, related_name = f'appears_in_form{case_form}')
    location = models.ForeignKey(Location, on_delete = models.SET_NULL, null = True, related_name = f"to_location_in_form{case_form}")
    produced = models.IntegerField()
    affiliation = models.ForeignKey(Location, on_delete=models.SET_NULL, null = True, related_name = f"to_affiliation_in_form{case_form}")
    
    class Meta: 
        abstract = False

class ImageCase(abstractModels.AbstractCase):
    case_form = 0
    form = abstractModels.AbstractCase.form(case_form)
    abstractModels.AbstractCase.accessed_by(case_form)

    associate = models.ForeignKey(UserModel.User, on_delete=models.SET_NULL, null = True)
    attendee = models.ManyToManyField(Personel, related_name = f'appears_in_form{case_form}')
    location = models.ForeignKey(Location, on_delete = models.SET_NULL, null = True, related_name = f"to_location_in_form{case_form}")
    produced = models.IntegerField()
    affiliation = models.ForeignKey(Location, on_delete=models.SET_NULL, null = True, related_name = f"to_affiliation_in_form{case_form}")
    
    class Meta: 
        abstract = False

class DocCase(abstractModels.AbstractCase):
    case_form = 2
    form = abstractModels.AbstractCase.form(case_form)
    abstractModels.AbstractCase.accessed_by(case_form)

    writer = models.ManyToManyField(Personel, related_name = 'wrote')
    referenced_personel = models.ManyToManyField(Personel, related_name = 'referenced_in')
    
    class Meta:
        abstract = False

