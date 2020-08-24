from django.contrib import admin
from .models import CustomUser, Sport, State, UnionTerritory, ProfilePicture

# Register your models here into admin
admin.site.register([
    CustomUser,
    Sport,
    UnionTerritory,
    State,
    ProfilePicture
])
