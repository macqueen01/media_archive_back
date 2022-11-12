from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)

admin.site.register(Personel)
admin.site.register(VideoCase)
admin.site.register(VideoMedia)
admin.site.register(Location)
admin.site.register(ImageMedia)
admin.site.register(ImageCase)
admin.site.register(AccessRequest)
admin.site.register(AccessRequestComponent)
admin.site.register(AuthorityRequest)



