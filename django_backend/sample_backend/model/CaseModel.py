from . import abstractModels
from . import UserModel
#from . import OrganizationModel
from django.db import models



class Location(abstractModels.AbstractCase):
    case_form = 4
    exec(abstractModels.AbstractCase.form(case_form))
    exec(abstractModels.AbstractCase.accessed_by(case_form))

    construction_date = models.DateTimeField(null = True, default = None)
    #connected_office = models.ManyToManyField(OrganizationModel.Organization, related_name="part_of")


class Personel(abstractModels.AbstractCase):
    case_form = 3
    exec(abstractModels.AbstractCase.form(case_form))
    exec(abstractModels.AbstractCase.accessed_by(case_form))

    birth_date = models.DateTimeField(null = True, default = None)
    affiliation = models.ForeignKey(Location, on_delete=models.SET_NULL, null = True)
    prefix = models.CharField(max_length=20, null = True)
    connected_account = models.ForeignKey(UserModel.User, on_delete=models.SET_NULL, null = True)


class VideoCase(abstractModels.AbstractCase):

    case_form = 1
    exec(abstractModels.AbstractCase.form(case_form))
    exec(abstractModels.AbstractCase.accessed_by(case_form))

    associate = models.ForeignKey(Personel, related_name = f'associated_in_form{case_form}', on_delete=models.SET_NULL, null = True)
    attendee = models.ManyToManyField(Personel, related_name = f'appears_in_form{case_form}')
    location = models.ForeignKey(Location, on_delete = models.SET_NULL, null = True, related_name = f"to_location_in_form{case_form}")
    produced = models.IntegerField()
    affiliation = models.ForeignKey(Location, on_delete=models.SET_NULL, null = True, related_name = f"to_affiliation_in_form{case_form}")

    
    class Meta: 
        abstract = False

class ImageCase(abstractModels.AbstractCase):
    case_form = 0
    exec(abstractModels.AbstractCase.form(case_form))
    exec(abstractModels.AbstractCase.accessed_by(case_form))

    associate = models.ForeignKey(Personel, related_name = f'associated_in_form{case_form}', on_delete=models.SET_NULL, null = True)
    attendee = models.ManyToManyField(Personel, related_name = f'appears_in_form{case_form}')
    location = models.ForeignKey(Location, on_delete = models.SET_NULL, null = True, related_name = f"to_location_in_form{case_form}")
    affiliation = models.ForeignKey(Location, on_delete=models.SET_NULL, null = True, related_name = f"to_affiliation_in_form{case_form}")
    produced = models.IntegerField()
    
    class Meta: 
        abstract = False

class DocCase(abstractModels.AbstractCase):
    case_form = 2
    exec(abstractModels.AbstractCase.form(case_form))
    exec(abstractModels.AbstractCase.accessed_by(case_form))

    writer = models.ManyToManyField(Personel, related_name = 'wrote')
    referenced_personel = models.ManyToManyField(Personel, related_name = 'referenced_in')
    
    class Meta:
        abstract = False

