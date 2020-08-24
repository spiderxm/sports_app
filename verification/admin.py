from django.contrib import admin
from .models import CustomUser, Sport, State, UnionTerritory, ProfilePicture, user_achievements

# Register your models here into admin
admin.site.register([
    CustomUser,
    Sport,
    UnionTerritory,
    State,
    ProfilePicture,
    user_achievements
])
