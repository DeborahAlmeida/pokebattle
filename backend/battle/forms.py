from django import forms
from pokemon.models import Pokemon
from .models import Battle, PokemonTeam, Team


class BattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['opponent', ]


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "pokemon_1",
            "pokemon_2",
            "pokemon_3",
        ]

    pokemon_1 = forms.ModelChoiceField(
        label="Pokemon 1",
        queryset=Pokemon.objects.all(),
        required=True,
    )
    pokemon_2 = forms.ModelChoiceField(
        label="Pokemon 2",
        queryset=Pokemon.objects.all(),
        required=True,
    )
    pokemon_3 = forms.ModelChoiceField(
        label="Pokemon 3",
        queryset=Pokemon.objects.all(),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self):
        data = self.clean()        
        battle_object = Battle.objects.get(pk=self.initial['battle'])
        if self.initial['user'] == 1:
            team = Team.objects.create(battle=battle_object, trainer=battle_object.creator)
        else:
            team = Team.objects.create(battle=battle_object, trainer=battle_object.opponent)
        PokemonTeam.objects.create(team=team, pokemon=Pokemon.objects.get(pokemon_id=18), order=1)
        PokemonTeam.objects.create(team=team, pokemon=Pokemon.objects.get(pokemon_id=16), order=2)
        PokemonTeam.objects.create(team=team, pokemon=Pokemon.objects.get(pokemon_id=15), order=3)
        teams = Team.objects.filter(battle=battle_object)
        if teams.count() > 1:
            battle_update = Battle.objects.filter(pk=self.initial['battle']).update(winner=battle_object.creator)
        instance = super().save(commit=False)
        return instance
