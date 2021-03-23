from django.contrib import admin
from .models import Gamer, Battle, Round, Status

admin.site.register(Gamer)
admin.site.register(Battle)
admin.site.register(Round)
admin.site.register(Status)