from django.contrib import admin

from .models import Car, Photo, Profile, Review, Avatar

# Register your models here
admin.site.register(Car)
admin.site.register(Photo)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Avatar)