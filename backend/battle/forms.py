from django import forms
from pokemon.models import Pokemon
from battle.models import Battle, PokemonTeam, Team
from battle.battles.battle import validate_sum_pokemons


class BattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['creator', 'opponent', ]

    def __init__(self, *args, **kwargs):
        super(BattleForm, self).__init__(*args, **kwargs)
        self.fields['creator'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['opponent'] == cleaned_data['creator']:
            raise forms.ValidationError("ERROR: You can't challenge yourself.")


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "battle",
            "trainer",
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
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['battle'].widget = forms.HiddenInput()
        self.fields['trainer'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        valid_pokemons = validate_sum_pokemons(
            [
                cleaned_data['pokemon_1'],
                cleaned_data['pokemon_2'],
                cleaned_data['pokemon_3']
            ]
        )
        obj_battle = cleaned_data['battle']
        if cleaned_data['trainer'] not in (obj_battle.creator, obj_battle.opponent):
            raise forms.ValidationError("ERROR: You do not have permission for this action.")

        if not valid_pokemons:
            raise forms.ValidationError("ERROR: Pokemons sum more than 600 points. Select again.")

        return cleaned_data

    def save(self, commit=True):
        data = self.clean()
        instance = super().save()
        PokemonTeam.objects.create(team=instance, pokemon=data['pokemon_1'], order=1)
        PokemonTeam.objects.create(team=instance, pokemon=data['pokemon_2'], order=2)
        PokemonTeam.objects.create(team=instance, pokemon=data['pokemon_3'], order=3)
        return instance
