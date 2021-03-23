from django import forms

from .models import Battle, Round

class BattleForm(forms.ModelForm):

    class Meta:
        model = Battle
        fields = ('player1', 'player2')

class RoundForm(forms.ModelForm):

    class Meta:
        model = Battle
        fields = ('player1', 'player2','pk11', 'pk21', 'pk31')


class RoundForm2(forms.ModelForm):

    class Meta:
        model = Battle
        fields = ('pk12', 'pk22', 'pk32')