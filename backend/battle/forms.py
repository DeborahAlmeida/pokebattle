from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string
from django.conf import settings

from battle.models import Battle, PokemonTeam, Team
from battle.battles.battle import validate_sum_pokemons, verify_pokemon_is_saved
from battle.battles.email import send_invite_email

from users.models import User

from pokemon.models import Pokemon

from pokemon.helpers import verify_pokemon_exists_api

POSITION_CHOICES = [(1, 1), (2, 2), (3, 3)]


class BattleForm(forms.ModelForm):
    opponent = forms.EmailField()

    class Meta:
        model = Battle
        fields = ['creator', 'opponent', ]

    def __init__(self, *args, **kwargs):
        super(BattleForm, self).__init__(*args, **kwargs)
        self.fields['creator'].widget = forms.HiddenInput()

    def clean_opponent(self):
        opponent_email = self.cleaned_data["opponent"]
        try:
            opponent = User.objects.get(email=opponent_email)
            opponent.is_guest = False
        except User.DoesNotExist:
            opponent = User.objects.create(email=opponent_email)
            opponent.is_guest = True
            random_password = get_random_string(length=64)
            opponent.set_password(random_password)
            opponent.save()
        return opponent

    def clean(self):
        cleaned_data = super().clean()
        if 'creator' not in cleaned_data:
            raise forms.ValidationError("ERROR: You need to be logged.")

        if 'opponent' not in cleaned_data:
            raise forms.ValidationError("ERROR: You need to choose an opponent")

        if cleaned_data['opponent'] == cleaned_data['creator']:
            raise forms.ValidationError("ERROR: You can't challenge yourself.")
        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.clean()
        instance = super().save()
        opponent = cleaned_data["opponent"]
        if opponent.is_guest:
            invite_form = PasswordResetForm(data={"email": opponent.email})
            invite_form.is_valid()
            invite_form.save(
                self, subject_template_name='registration/guest_email_subject.txt',
                email_template_name='registration/guest_email.html',
                from_email=settings.FROM_EMAIL,)
        else:
            send_invite_email(instance.opponent, instance.creator)
        return instance


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "battle",
            "trainer",
            "pokemon_1",
            "pokemon_2",
            "pokemon_3",
            "position_pkn_1",
            "position_pkn_2",
            "position_pkn_3",
        ]

    battle = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Battle.objects.all())
    trainer = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=User.objects.all())
    position_pkn_1 = forms.ChoiceField(choices=POSITION_CHOICES, label="Position")
    position_pkn_2 = forms.ChoiceField(choices=POSITION_CHOICES, label="Position")
    position_pkn_3 = forms.ChoiceField(choices=POSITION_CHOICES, label="Position")
    pokemon_1 = forms.CharField(widget=forms.Textarea)
    pokemon_2 = forms.CharField(widget=forms.Textarea)
    pokemon_3 = forms.CharField(widget=forms.Textarea)

    def clean(self):
        # import ipdb; ipdb.set_trace()
        cleaned_data = super().clean()
        pokemon_1 = self.cleaned_data.get('pokemon_1')
        pokemon_2 = self.cleaned_data.get('pokemon_2')
        pokemon_3 = self.cleaned_data.get('pokemon_3')
        obj_battle = cleaned_data['battle']
        obj_trainer = cleaned_data['trainer']
        position_pkn_1 = cleaned_data['position_pkn_1']
        position_pkn_2 = cleaned_data['position_pkn_2']
        position_pkn_3 = cleaned_data['position_pkn_3']

        if not pokemon_1 or not pokemon_2 or not pokemon_3:
            raise forms.ValidationError('ERROR: Select all pokemons')

        if not position_pkn_1 or not position_pkn_2 or not position_pkn_3:
            raise forms.ValidationError('ERROR: Select all positions')

        pokemons_exist = verify_pokemon_exists_api([pokemon_1, pokemon_2, pokemon_3])
        if not pokemons_exist:
            raise forms.ValidationError('ERROR: Type the correct pokemons name ')

        valid_pokemons = validate_sum_pokemons(
            [
                cleaned_data['pokemon_1'],
                cleaned_data['pokemon_2'],
                cleaned_data['pokemon_3']
            ]
        )
        if obj_trainer not in (obj_battle.creator, obj_battle.opponent):
            raise forms.ValidationError("ERROR: You do not have permission for this action.")

        if not valid_pokemons:
            raise forms.ValidationError("ERROR: Pokemons sum more than 600 points. Select again.")

        if position_pkn_1 in (position_pkn_2, position_pkn_3):
            raise forms.ValidationError('ERROR: You cannot add the same position')
        if position_pkn_2 == position_pkn_3:
            raise forms.ValidationError('ERROR: You cannot add the same position')

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
        cleaned_data = self.clean()
        instance = super().save()

        PokemonTeam.objects.create(
            team=instance,
            pokemon=cleaned_data['pokemon_1_object'],
            order=cleaned_data['position_pkn_1'])

        PokemonTeam.objects.create(
            team=instance,
            pokemon=cleaned_data['pokemon_2_object'],
            order=cleaned_data['position_pkn_2'])

        PokemonTeam.objects.create(
            team=instance,
            pokemon=cleaned_data['pokemon_3_object'],
            order=cleaned_data['position_pkn_3'])
        return instance


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )
