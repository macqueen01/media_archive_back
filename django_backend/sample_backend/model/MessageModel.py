from . import UserModel
from . import RequestModel
from django.db import models
from django.utils import timezone


class MessageManager(models.Manager):


    def delete_message(self, message_obj):
        # this hides the message from the receiver
        message_obj.hidden = 1
        message_obj.save()
        return True

    def get_rejections(self):
        pass

    def get_admissions(self):
        pass

    def get_messages_related_user(self, user_id):
        q = models.Q()
        q.add(models.Q(hidden__exact = 0), q.AND)
        q.add(models.Q(receiver__id__exact = user_id) | 
            models.Q(sender__id__exact = user_id), q.AND)
        return self.filter(q)

    def get_messages_received_by_user(self, user_id):
        q = models.Q()
        q.add(models.Q(hidden__exact = 0), q.AND)
        q.add(models.Q(receiver__id__exact = user_id), q.AND)
        return self.filter(q)

    def get_messages_sent_by_user(self, user_id):
        q = models.Q()
        q.add(models.Q(hidden__exact = 0), q.AND)
        q.add(models.Q(sender__id__exact = user_id), q.AND)
        return self.filter(q)

    def send(self, sender, receiver_set, content, message_type = 2):
        # message_type == 2 -> the most normal and simple message type, no connected actions taken
        # message_type == 1 -> this should indicate acceptance of a request. connected to the request object through foreign key
        # message_type == 0 -> this should indicate rejection of a request. connected to the request object through foreign key
        # postpone -> this method should be implemented for both single receiver argument and multiple receivers argument.
        

        def create_message(receiver):
            new_message = self.model(
                sender = sender,
                receiver = receiver,
                content = content,
                created_at = timezone.now(),
                message_type = message_type
            )
            new_message.save()
            return new_message

        is_queryset = isinstance(receiver_set, models.query.QuerySet)
        message_list = []

        if not is_queryset:
            receiver = receiver_set
            new_message = create_message(receiver)
            message_list.append(new_message)
            return message_list

        for receiver in receiver_set:
            new_message = create_message(receiver)
            message_list.append(new_message)
        
        return message_list

    def visible_messages(self, receiver):
        # messages that are not deleted
        pass

class Message(models.Model):
    sender = models.ForeignKey(UserModel.User, on_delete = models.SET_NULL, null = True, related_name = "message_sent")
    receiver = models.ForeignKey(UserModel.User, on_delete = models.SET_NULL, null = True, related_name = "message_received")
    content = models.TextField()
    hidden = models.IntegerField(default = 0)
    created_at = models.DateTimeField()
    message_type = models.IntegerField()

    objects = MessageManager()


        



