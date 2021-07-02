from django import forms
from django.contrib.auth.forms import UserCreationForm

from battle.models import Battle, PokemonTeam, Team
from battle.battles.battle import validate_sum_pokemons, get_pokemon_object, verify_pokemon_is_saved

from users.models import User

from pokemon.models import Pokemon

from dal import autocomplete


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

    battle = forms.CharField(widget=forms.Textarea)
    trainer = forms.CharField(widget=forms.Textarea)
    pokemon_1 = forms.CharField(widget=forms.Textarea)
    pokemon_2 = forms.CharField(widget=forms.Textarea)
    pokemon_3 = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        valid_pokemons = validate_sum_pokemons(
            [
                cleaned_data['pokemon_1'],
                cleaned_data['pokemon_2'],
                cleaned_data['pokemon_3']
            ]
        )
        cleaned_data['battle_object'] = Battle.objects.get(id=cleaned_data['battle'])

        if cleaned_data['trainer'] not in (cleaned_data['battle_object'].creator, cleaned_data['battle_object'].opponent):
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


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )

