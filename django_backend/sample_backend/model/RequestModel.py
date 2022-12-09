from django.db import models
from . import abstractModels
from django.utils import timezone
from sample_backend.view.utilities import check_user_level
from . import CaseModel
from . import UserModel

class AuthorityRequestManager(abstractModels.RequestManager):

    def open_request(
        self,
        user,
        title,
        comments,
        auth_from,
        auth_to
        ):

        if (check_user_level(user)) and (auth_to in [0,1,2]):
            auth_from = check_user_level(user)
        else:
            return False

        request = self.model(
            request_form1_requested_by = user,
            title = title,
            comments = comments,
            auth_from = auth_from,
            auth_to = auth_to,
            created_at = timezone.now()
        )

        request.save()
        return request




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

    objects = AuthorityRequestManager()



class AccessRequestComponent(models.Model):
    requesting_case_form = models.IntegerField()

    image_case = models.ForeignKey(CaseModel.ImageCase, on_delete = models.SET_NULL, related_name = "access_requested", null = True)
    video_case = models.ForeignKey(CaseModel.VideoCase, on_delete = models.SET_NULL, related_name = "access_requested", null = True)
    doc_case = models.ForeignKey(CaseModel.DocCase, on_delete = models.SET_NULL, related_name = "access_requested", null = True)

    status = models.IntegerField(default = 2)


class AccessRequestManager(abstractModels.RequestManager):

    def open_request(
        self,
        user,
        title,
        comments,
        case_id_map
    ):

        # IMPORTANT! this model method doesn't undo when error 
        # occurs inside request component creation. 
        # This really needs an implementation for try and except

        request = self.model(
            request_form0_requested_by = user,
            title = title,
            comments = comments,
            created_at = timezone.now()
        )

        request.save()

        for case_form in case_id_map.keys():
            if case_form == 0:
                image_cases = case_id_map[case_form]
                for id in image_cases:
                    case = CaseModel.ImageCase.objects.filter(id = id).get()
                    request_comp = AccessRequestComponent(
                        requesting_case_form = 0,
                        image_case = case
                    )
                    request_comp.save()
                    request.request_components.add(request_comp)
                    request.save()

            elif case_form == 1:
                video_cases = case_id_map[case_form]
                for id in video_cases:
                    case = CaseModel.VideoCase.objects.filter(id = id).get()
                    request_comp = AccessRequestComponent(
                        requesting_case_form = 1,
                        video_case = case
                    )
                    request_comp.save()
                    request.request_components.add(request_comp)
                    request.save()

            elif case_form == 2:
                doc_cases = case_id_map[case_form]
                for id in doc_cases:
                    case = CaseModel.DocCase.objects.filter(id = id).get()
                    request_comp = AccessRequestComponent(
                        requesting_case_form = 2,
                        doc_case = case
                    )
                    request_comp.save()
                    request.request_components.add(request_comp)
                    request.save()
        
        return True
            
            


class AccessRequest(abstractModels.AbstractRequest):
    is_authority = 0
    exec(abstractModels.AbstractRequest.requested_by(is_authority))
    exec(abstractModels.AbstractRequest.form(is_authority))

    request_components = models.ManyToManyField(AccessRequestComponent, related_name = "requested_in")

    # Status in AccessRequest changes when manager decides to change the status
    # without viewing the detailed view of the request content.

    status = models.IntegerField(default = 2)

    objects = AccessRequestManager()


