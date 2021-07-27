from django.contrib import admin
from battle.tasks import run_battle_and_send_result_email
from .models import Battle, Team, PokemonTeam


class PokemonsInline(admin.TabularInline):
    model = PokemonTeam
    extra = 1


class TeamAdmin(admin.ModelAdmin):
    inlines = (PokemonsInline,)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        run_battle_and_send_result_email.delay(obj.battle_id)


admin.site.register(Battle)
admin.site.register(Team, TeamAdmin)
admin.site.register(PokemonTeam)
