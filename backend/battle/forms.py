from django import forms

from .models import Battle, PokemonTeam, Team
from pokemon.models import Pokemon

class TeamForm(forms.ModelForm):
    class Meta:
        model = PokemonTeam
        fields = [
        'pokemon_1',
        'pokemon_2',
        'pokemon_3'
        ]

    pokemon_1 = forms.IntegerField(
        label= "Pokemon 1"
    )
    
    pokemon_2 = forms.IntegerField(
        label= "Pokemon 2"
    )

    pokemon_3 = forms.IntegerField(
        label= "Pokemon 3"
    )
    
    # def save(self, commit=True):
    #     PokemonTeam.objects.create(team=Team.objects.get(pk=47), pokemon=Pokemon.objects.get(pokemon_id=18), order=1)
    #     PokemonTeam.objects.create(team=Team.objects.get(pk=47), pokemon=Pokemon.objects.get(pokemon_id=16), order=2)
    #     PokemonTeam.objects.create(team=Team.objects.get(pk=47), pokemon=Pokemon.objects.get(pokemon_id=15), order=3)
    #     instance = super().save(commit=False)
    #     instance.some_flag = True
    #     if commit:
    #         instance.save()
    #         self.save_m2m()

    #     return instance


# class BattleForm(forms.ModelForm):

#     class Meta:
#         model = Battle
#         fields = ('opponent')

# class RoundForm(forms.ModelForm):

#     class Meta:
#         model = Battle
#         fields = ('creator', 'opponent', 'pk1_creator', 'pk2_creator', 'pk3_creator')


# class RoundForm2(forms.ModelForm):

#     class Meta:
#         model = Battle
#         fields = ('pk1_opponent', 'pk2_opponent', 'pk3_opponent')
