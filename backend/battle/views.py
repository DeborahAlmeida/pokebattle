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

#email
from templated_email import get_templated_mail



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
            if (sumAll <= 600):
                pokemons = [round_opponent.pk1_opponent, round_opponent.pk2_opponent, round_opponent.pk3_opponent]
                result = battleRunning(53, pokemons)
                #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>result", result)
                round_opponent.winner = result
                round_opponent.save()
                sendEmail()

                return redirect('home')
            if (sumAll > 600): 
                message = "ERROR: The PKNs you selected sum more than 600 points, please choose again"
                return render(request, 'battle/round_new2.html', {'formRound2': formRound2, 'battle':battleInfo, 'message': message})
    else:
        formRound2 = RoundForm2()
    return render(request, 'battle/round_new2.html', {'formRound2': formRound2, 'battle':battleInfo})


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

def roundRunning(info):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",info)

    pokemon_creator = info[0]
    pokemon_opponent = info[1]

    winner = "nobody"
    opponent = 0
    creator = 0
    if (pokemon_creator["attack"] > pokemon_opponent["defense"] ):
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pokeInfo1_creator[attack]:", pokeInfo1_creator["attack"])
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pokeInfo1_opponent[defense]:", pokeInfo1_opponent["defense"])
        creator = creator + 1
        winnerRoundOne = "creator"
    if (pokemon_creator["attack"] == pokemon_opponent["defense"] ):
        creator = creator + 1
        opponent = opponent + 1
        winnerRoundOne = "nobody"
    else:
        winnerRoundOne = "opponent"
        opponent = opponent + 1

    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pokeInfo2_opponent[attack]:", pokeInfo2_opponent["attack"])
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pokeInfo2_creator[defense]:", pokeInfo2_creator["defense"])

    if (pokemon_opponent["attack"] > pokemon_creator["defense"] ):
            winnerRoundTwo = "opponent"
            opponent = opponent + 1
    if (pokemon_opponent["attack"] == pokemon_creator["defense"] ):
        creator = creator + 1
        opponent = opponent + 1
        winnerRoundTwo = "nobody"
    else:
        winnerRoundTwo = "creator"
        creator = creator + 1

    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pokeInfo2_opponent[hp]:", pokeInfo2_opponent["hp"])
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pokeInfo2_creator[hp]:", pokeInfo2_creator["hp"])

    if (creator > opponent):
        winner = "creator"
    elif (creator < opponent):
        winner = "opponent"
    elif (creator == opponent):
        if (pokemon_opponent["hp"] > pokemon_creator["hp"] ):
            winner = "opponent"
            opponent = opponent + 1
        elif (pokemon_opponent["hp"] < pokemon_creator["hp"] ):
            winner = "creator"
        else: 
            creator = creator + 1
            opponent = opponent + 1
            winnerRoundTwo = "nobody"
    
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>aqui", creator, opponent, winner)

    if (creator > opponent):
        winner = "creator"
    elif (creator < opponent):
        winner = "opponent"
    else:
        winner = "creator"

    return winner



def battleRunning(poke_id, pokemons):
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", pokemons[0])
    battleInfo = Battle.objects.get(id = poke_id)
    pokeInfo1_creator = get_pokemon_from_api(battleInfo.pk1_creator)
    pokeInfo2_creator = get_pokemon_from_api(battleInfo.pk2_creator)
    pokeInfo3_creator = get_pokemon_from_api(battleInfo.pk3_creator)
    pokeInfoCreatorList = [pokeInfo1_creator, pokeInfo2_creator, pokeInfo3_creator]
    pokeInfo1_opponent = get_pokemon_from_api(pokemons[0])
    pokeInfo2_opponent = get_pokemon_from_api(pokemons[1])
    pokeInfo3_opponent = get_pokemon_from_api(pokemons[2])

    roundOne = [pokeInfo1_creator, pokeInfo1_opponent]
    roundTwo = [pokeInfo2_creator, pokeInfo2_opponent]
    roundThree = [pokeInfo3_creator, pokeInfo3_opponent]

    winner = "nobody"
    opponent = 0
    creator = 0

    battleRounds = [roundOne, roundTwo, roundThree ]

    for battleRound in battleRounds: 
        result = roundRunning(battleRound)
        if result == "creator":
            creator = creator + 1
        else:
            opponent = opponent + 1

    if (creator > opponent):
        winner = "creator"
    elif (creator < opponent):
        winner = "opponent"
    else:
        winner = "creator"

    return winner
        

'''
result = battleRunning(53)
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>winner on def:", formRound2)
                formRound2.winner = battleRunning(53)
'''

def sendEmail():
    get_templated_mail(
            template_name='results_battle',
            from_email='deborahmendonca6@gmail.com',
            to=['deborahsoares01@gmail.com'],
            context={
                'username':"teste",
                'full_name':"teste",
                'signup_date':"teste"
            },
            # Optional:
            # cc=['cc@example.com'],
            # bcc=['bcc@example.com'],
            # headers={'My-Custom-Header':'Custom Value'},
            # template_prefix="my_emails/",
            # template_suffix="email",
    )