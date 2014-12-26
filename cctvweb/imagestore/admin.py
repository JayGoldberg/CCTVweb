from django.contrib import admin
from imagestore.models import Camera,Image,Tag

# Register your models here.
admin.site.register(Camera)
admin.site.register(Image)
admin.site.register(Tag)
