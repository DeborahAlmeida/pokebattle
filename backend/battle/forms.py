from django import forms

from .models import Battle, PokemonTeam, Team
from pokemon.models import Pokemon


class BattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['opponent',]


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


    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
            
        
    def save(self, commit=True):
        data = self.clean()
        team = Team.objects.get(pk=143)
        team.pokemons.add(data["pokemon_1"])
        team.pokemons.add(data["pokemon_2"])
        team.pokemons.add(data["pokemon_3"])
        PokemonTeam.objects.filter(team=team, pokemon=data["pokemon_1"]).update(order=1)
        PokemonTeam.objects.filter(team=team, pokemon=data["pokemon_2"]).update(order=2)
        PokemonTeam.objects.filter(team=team, pokemon=data["pokemon_3"]).update(order=3)
        instance = super().save(commit=False)
        instance.some_flag = True
        return instance
