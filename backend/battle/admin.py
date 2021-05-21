from django.contrib import admin
from .models import Battle, Team, PokemonTeam


class PokemonsInline(admin.TabularInline):
    model = PokemonTeam
    extra = 1


class TeamAdmin(admin.ModelAdmin):
    inlines = (PokemonsInline,)


admin.site.register(Battle)
admin.site.register(Team, TeamAdmin)
admin.site.register(PokemonTeam)

