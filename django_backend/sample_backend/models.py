from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length = 20)
    affiliation = models.CharField(max_length = 20)
    created_at = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to = 'image/%Y%m%d', blank = True)

    def __str__(self):
        return self.name

class Case(models.Model):
    case_type = models.CharField(max_length = 10)
    uploader = models.CharField(max_length = 10)
    associate = models.CharField(max_length = 10)
    location = models.CharField(max_length = 10)
    collected = models.IntegerField(default = 0)
    private = models.IntegerField(default = 0)
    attendee = models.CharField(max_length = 20)
    created_at = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    src = models.ImageField(upload_to="image/%Y%m%d")

    def __str__(self):
        return self.title

    

