from django.db import models
from django.utils import timezone
# imports all models inside 'model' file
from .model.UserModel import User 
from .model.CaseModel import VideoCase, ImageCase, DocCase, Location, Personel
from .model.MediaModel import VideoMedia, ImageMedia, DocMedia
from .model.RequestModel import AccessRequest, AccessRequestComponent, AuthorityRequest
from .model.MessageModel import Message

# Create your models here.


    

