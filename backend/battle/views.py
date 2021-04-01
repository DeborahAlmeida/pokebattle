#available to pull request
from django.shortcuts import render
from django.shortcuts import redirect
import requests
from urllib.parse import urljoin
from .models import Gamer, Battle
from .forms import BattleForm, RoundForm, RoundForm2
from django.conf import settings
from .battles.rounds import battleRunning


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
    url = urljoin(settings.POKE_API_URL, "?limit=1118")
    response = requests.get(url)
    data = response.json()
    listPokemon = []
    for pokemon in data["results"]:
        listPokemon.append(pokemon["name"])
        
    if request.method == "POST":
        formRound = RoundForm(request.POST)
        if formRound.is_valid():
            roundBattle = formRound.save(commit=False)
            dataPK11 = get_pokemon_from_api(roundBattle.pk1_creator)
            dataPK21 = get_pokemon_from_api(roundBattle.pk2_creator)
            dataPK31 = get_pokemon_from_api(roundBattle.pk3_creator)
            sumPK11 = sumValid(dataPK11)
            sumPK21 = sumValid(dataPK21)
            sumPK31 = sumValid(dataPK31)
            sumAll = sumPK11 + sumPK21 + sumPK31
            if sumAll <= 600:
                roundBattle.save()
                return redirect('invite')
            if sumAll > 600: 
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
    battleInfo = Battle.objects.latest('id')
    if request.method == "POST":
        formRound2 = RoundForm2(request.POST, instance=battleInfo)
        if formRound2.is_valid():
            round_opponent = formRound2.save(commit=False)
            dataPK11 = get_pokemon_from_api(round_opponent.pk1_opponent)
            dataPK21 = get_pokemon_from_api(round_opponent.pk2_opponent)
            dataPK31 = get_pokemon_from_api(round_opponent.pk3_opponent)
            sumPK11 = sumValid(dataPK11)
            sumPK21 = sumValid(dataPK21)
            sumPK31 = sumValid(dataPK31)
            sumAll = sumPK11 + sumPK21 + sumPK31
            currentId = battleInfo.id
            if sumAll <= 600:
                pokemons = [round_opponent.pk1_opponent, round_opponent.pk2_opponent, round_opponent.pk3_opponent]
                result = battleRunning(currentId, pokemons)
                round_opponent.winner = result
                round_opponent.save()

                return redirect('home')
            if (sumAll > 600): 
                message = "ERROR: The PKNs you selected sum more than 600 points, please choose again"
                return render(request, 'battle/round_new2.html', {'formRound2': formRound2, 'battle': battleInfo, 'message': message})
    else:
        formRound2 = RoundForm2()
    return render(request, 'battle/round_new2.html', {'formRound2': formRound2, 'battle': battleInfo})


def get_pokemon_from_api(poke_id):
    url = urljoin(settings.POKE_API_URL, poke_id)
    response = requests.get(url)
    data = response.json()
        
    info = {
        "defense": data["stats"][2]["base_stat"],
        "attack": data["stats"][1]["base_stat"],
        "hp": data["stats"][0]["base_stat"],
    }
    return info


def sumValid(pokemon):
    sumResult = pokemon["attack"] +  pokemon["defense"] + pokemon["hp"]
    return sumResult
