from django.db import models
from . import abstractModels
from . import CaseModel
from . import UserModel



class AuthorityRequest(abstractModels.AbstractRequest):
    is_authority = 1

    # These execution lines reference UserModel
    exec(abstractModels.AbstractRequest.requested_by(is_authority))
    exec(abstractModels.AbstractRequest.form(is_authority))

    auth_from = models.IntegerField()
    auth_to = models.IntegerField()

    # STATUS TABLE
    # 2: pending
    # 1: accepted
    # 0: rejected
    status = models.IntegerField(default = 2)



class AccessRequestComponent(models.Model):
    requesting_case_form = models.IntegerField()

    image_case = models.ForeignKey(CaseModel.ImageCase, on_delete = models.SET_NULL, related_name = "access_requested", null = True)
    video_case = models.ForeignKey(CaseModel.VideoCase, on_delete = models.SET_NULL, related_name = "access_requested", null = True)
    doc_case = models.ForeignKey(CaseModel.DocCase, on_delete = models.SET_NULL, related_name = "access_requested", null = True)

    status = models.IntegerField(default = 2)




class AccessRequest(abstractModels.AbstractRequest):
    is_authority = 0
    exec(abstractModels.AbstractRequest.requested_by(is_authority))
    exec(abstractModels.AbstractRequest.form(is_authority))

    request_components = models.ManyToManyField(AccessRequestComponent, related_name = "requested_in")

    # Status in AccessRequest changes when manager decides to change the status
    # without viewing the detailed view of the request content.


