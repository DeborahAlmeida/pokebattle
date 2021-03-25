from django import forms

from .models import Battle, Round

class BattleForm(forms.ModelForm):

    class Meta:
        model = Battle
        fields = ('creator', 'opponent')

class RoundForm(forms.ModelForm):

    class Meta:
        model = Battle
        fields = ('creator', 'opponent','pk1_creator', 'pk2_creator', 'pk3_creator')


class RoundForm2(forms.ModelForm):

    class Meta:
        model = Battle
        fields = ('pk1_opponent', 'pk2_opponent', 'pk3_opponent')