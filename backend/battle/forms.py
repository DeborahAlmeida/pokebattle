from django import forms
from battle.models import Battle, PokemonTeam, Team
from battle.battles.battle import validate_sum_pokemons, get_pokemon_object, verify_pokemon_is_saved


class BattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['creator', 'opponent', ]

    def __init__(self, *args, **kwargs):
        super(BattleForm, self).__init__(*args, **kwargs)
        self.fields['creator'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        if 'creator' not in cleaned_data:
            raise forms.ValidationError("ERROR: You need to be logged.")

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

    pokemon_1 = forms.IntegerField(
        label="Pokemon 1",
        required=True,
        min_value=1,
        max_value=898,
    )
    pokemon_2 = forms.IntegerField(
        label="Pokemon 2",
        required=True,
        min_value=1,
        max_value=898,
    )
    pokemon_3 = forms.IntegerField(
        label="Pokemon 3",
        required=True,
        min_value=1,
        max_value=898,
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

        verify_pokemon_is_saved(
            [
                cleaned_data['pokemon_1'],
                cleaned_data['pokemon_2'],
                cleaned_data['pokemon_3']
            ]
        )

        cleaned_data['pokemon_1_object'] = get_pokemon_object(cleaned_data['pokemon_1'])
        cleaned_data['pokemon_2_object'] = get_pokemon_object(cleaned_data['pokemon_2'])
        cleaned_data['pokemon_3_object'] = get_pokemon_object(cleaned_data['pokemon_3'])
        return cleaned_data

    def save(self, commit=True):
        data = self.clean()
        instance = super().save()
        PokemonTeam.objects.create(team=instance,
                                   pokemon=data['pokemon_1_object'], order=1)
        PokemonTeam.objects.create(team=instance,
                                   pokemon=data['pokemon_2_object'], order=2)
        PokemonTeam.objects.create(team=instance,
                                   pokemon=data['pokemon_3_object'], order=3)
        return instance
