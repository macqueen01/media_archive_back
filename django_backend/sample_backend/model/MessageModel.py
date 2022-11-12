from . import UserModel
from . import RequestModel
from django.db import models


class MessageManager(models.Manager):


    def delete_message(self, message_obj):
        # this hides the message from the receiver
        pass

    def get_rejections(self):
        pass

    def get_admissions(self):
        pass

    def get_messages_from_user(self, user_id):
        pass

    def get_messages_received_by_user(self, user_id):
        pass

    def get_messages_sent_by_user(self, user_id):
        pass

    def send(self, sender, receiver_set, content, message_type = 2):
        # message_type == 2 -> the most normal and simple message type, no connected actions taken
        # message_type == 1 -> this should indicate acceptance of a request. connected to the request object through foreign key
        # message_type == 0 -> this should indicate rejection of a request. connected to the request object through foreign key
        # postpone -> this method should be implemented for both single receiver argument and multiple receivers argument.
        
        pass

    def visible_messages(self, receiver):
        # messages that are not deleted
        pass

class MessageModel(models.Model):
    sender = models.ForeignKey(UserModel.User, on_delete = models.SET_NULL, null = True, related_name = "message_sent")
    receiver = models.ForeignKey(UserModel.User, on_delete = models.SET_NULL, null = True, related_name = "message_received")
    content = models.TextField()
    created_at = models.DateTimeField()
    message_type = models.IntegerField()

    objects = MessageManager()


        



