from django.contrib import admin
from .models import User, Case, Location, Personel, VideoCase, ImageCase, DocCase, VideoMedia, ImageMedia, DocMedia

# Register your models here.

admin.site.register(User)
admin.site.register(Case)
admin.site.register(Personel)
admin.site.register(VideoCase)
admin.site.register(VideoMedia)
admin.site.register(Location)



