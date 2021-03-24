from django.shortcuts import render
from django.shortcuts import redirect
#from .models import Gamer
from users.models import User
from .models import Gamer, Battle
from .forms import BattleForm, RoundForm, RoundForm2

from django.utils.html import format_html
from django.contrib import messages

from urllib.parse import urljoin

import requests
#from progress.bar import ChargingBar
from django.conf import settings


# Create your views here.
def home(request):
    gamer = Gamer.objects.all()
    return render(request, 'battle/home.html', { 'gamer' : gamer})

def battle_new(request):
    if request.method == "POST":
        form = BattleForm(request.POST)
        if form.is_valid():
            battle = form.save(commit=False)
            battle.save()
            return redirect('round_new')
    else:
        form = BattleForm()
    return render(request, 'battle/battle_edit.html', {'form': form})

def round_new(request):
    url = urljoin(settings.POKE_API_URL, "?limit=20")
    response = requests.get(url)
    data = response.json()
    listPokemon = []
    for pokemon in data["results"]:
        listPokemon.append(pokemon["name"])
        
    if request.method == "POST":
        formRound = RoundForm(request.POST)
        if formRound.is_valid():
            roundBattle = formRound.save(commit=False)
            dataPK11 = get_pokemon_from_api(roundBattle.pk11)
            dataPK21 = get_pokemon_from_api(roundBattle.pk21)
            dataPK31 = get_pokemon_from_api(roundBattle.pk31)
            sumPK11 = sumValid(dataPK11)
            sumPK21 = sumValid(dataPK21)
            sumPK31 = sumValid(dataPK31)
            sumAll = sumPK11 + sumPK21 + sumPK31
            if (sumAll <= 600):
                roundBattle.save()
                return redirect('invite')
            if (sumAll > 600): 
                message = "ERROR: The PKNs you selected sum more than 600 points, please choose again"
                return render(request, 'battle/round_new.html', {'formRound': formRound, 'message': message})
    else:
        formRound = RoundForm()
    return render(request, 'battle/round_new.html', {'formRound': formRound})

def invite(request):
    return render(request, 'battle/invite.html')

def player2(request):
    return render(request, 'battle/opponent.html')

def round_new2(request):
    battleInfo = Battle.objects.get(id=43)
    if request.method == "POST":
        formRound2 = RoundForm2(request.POST, instance=battleInfo)
        if formRound2.is_valid():
            teste = formRound2.save(commit=False)
            dataPK11 = get_pokemon_from_api(teste.pk12)
            dataPK21 = get_pokemon_from_api(teste.pk22)
            dataPK31 = get_pokemon_from_api(teste.pk32)
            sumPK11 = sumValid(dataPK11)
            sumPK21 = sumValid(dataPK21)
            sumPK31 = sumValid(dataPK31)
            sumAll = sumPK11 + sumPK21 + sumPK31
            if (sumAll <= 600):
                formRound2.save()
                return redirect('home')
            if (sumAll > 600): 
                message = "ERROR: The PKNs you selected sum more than 600 points, please choose again"
                return render(request, 'battle/round_new2.html', {'formRound2': formRound2, 'battle':battleInfo, 'message': message})
    else:
        formRound2 = RoundForm2()
    return render(request, 'battle/round_new2.html', {'formRound2': formRound2, 'battle':battleInfo})


def get_pokemon_from_api(poke_name):
    url = urljoin(settings.POKE_API_URL, poke_name)
    response = requests.get(url)
    data = response.json()
    info = {
        "defense": data["stats"][3]["base_stat"],
        "attack": data["stats"][4]["base_stat"],
        "hp": data["stats"][5]["base_stat"],
    }
    return info


def sumValid(pokemon):
    sumResult = pokemon["attack"] +  pokemon["defense"] + pokemon["hp"]
    return sumResult
