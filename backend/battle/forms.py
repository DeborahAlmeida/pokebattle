from django import forms
import requests
from urllib.parse import urljoin
import requests
from urllib.error import HTTPError
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm

from battle.models import Battle, PokemonTeam, Team
from battle.battles.battle import validate_sum_pokemons, get_pokemon_object, verify_pokemon_is_saved

from users.models import User

from pokemon.models import Pokemon


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

    battle = forms.ModelChoiceField(queryset=Battle.objects.all())
    trainer = forms.ModelChoiceField(queryset=User.objects.all())
    pokemon_1 = forms.CharField(widget=forms.Textarea)
    pokemon_2 = forms.CharField(widget=forms.Textarea)
    pokemon_3 = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        pokemon_1 = self.cleaned_data.get('pokemon_1')
        pokemon_2 = self.cleaned_data.get('pokemon_2')
        pokemon_3 = self.cleaned_data.get('pokemon_3')

        if not pokemon_1 or not pokemon_2 or not pokemon_3:
            raise forms.ValidationError('ERROR: Select all pokemons')

        for pokemon in [pokemon_1, pokemon_2, pokemon_3]:
            response = requests.get(urljoin(settings.POKE_API_URL, pokemon))
            if response.status_code == 404:
                raise forms.ValidationError('ERROR: Type the correct pokemon name ')

        valid_pokemons = validate_sum_pokemons(
            [
                cleaned_data['pokemon_1'],
                cleaned_data['pokemon_2'],
                cleaned_data['pokemon_3']
            ]
        )

        if cleaned_data['trainer'] not in (cleaned_data['battle'].creator, cleaned_data['battle'].opponent):
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
        cleaned_data['pokemon_1_object'] = Pokemon.objects.get(name=cleaned_data['pokemon_1'])
        cleaned_data['pokemon_2_object'] = Pokemon.objects.get(name=cleaned_data['pokemon_2'])
        cleaned_data['pokemon_3_object'] = Pokemon.objects.get(name=cleaned_data['pokemon_3'])
        return cleaned_data

    def save(self, commit=True):
        data = self.clean()
        instance = Team.objects.create(battle=data['battle'], trainer=data['trainer'])
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

