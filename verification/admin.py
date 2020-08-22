from django.contrib import admin
from .models import CustomUser, Sport, State, UnionTerritory

# Register your models here.
admin.site.register([
    CustomUser,
    Sport,
    UnionTerritory,
    State
])
