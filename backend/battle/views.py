from django.shortcuts import render
from django.shortcuts import redirect
from urllib.parse import urljoin
import requests
from .models import Gamer, Battle
from .forms import BattleForm, RoundForm, RoundForm2
from django.conf import settings
from .battles.battle import battleRunning
from .battles.pokemon import get_pokemon_from_api


def home(request):
    return render(request, 'battle/home.html')


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
    if request.method == "POST":
        form_round = RoundForm(request.POST)
        if form_round.is_valid():
            round_battle = form_round.save(commit=False)
            data_pk11 = get_pokemon_from_api(round_battle.pk1_creator)
            data_pk21 = get_pokemon_from_api(round_battle.pk2_creator)
            data_pk31 = get_pokemon_from_api(round_battle.pk3_creator)
            sum_pk11 = sumValid(data_pk11)
            sum_pk21 = sumValid(data_pk21)
            sum_pk31 = sumValid(data_pk31)
            if (sum_pk11 + sum_pk21 + sum_pk31) <= 600:
                round_battle.save()
                return redirect('invite')
            if (sum_pk11 + sum_pk21 + sum_pk31) > 600:
                message = "ERROR: PKNs you selected sum more than 600 points, please choose again"
                return render(request, 'battle/round_new.html', {'form_round': form_round,
                                                                'message': message})
    else:
        form_round = RoundForm()
    return render(request, 'battle/round_new.html', {'form_round': form_round})


def invite(request):
    return render(request, 'battle/invite.html')


def player2(request):
    return render(request, 'battle/opponent.html')


def round_new2(request):
    battle_info = Battle.objects.latest('id')
    if request.method == "POST":
        form_round2 = RoundForm2(request.POST, instance=battle_info)
        if form_round2.is_valid():
            round_opponent = form_round2.save(commit=False)
            data_pk11 = get_pokemon_from_api(round_opponent.pk1_opponent)
            data_pk21 = get_pokemon_from_api(round_opponent.pk2_opponent)
            data_pk31 = get_pokemon_from_api(round_opponent.pk3_opponent)
            sum_pk11 = sumValid(data_pk11)
            sum_pk21 = sumValid(data_pk21)
            sum_pk31 = sumValid(data_pk31)
            current_id = battle_info.id
            if (sum_pk11 + sum_pk21 + sum_pk31) <= 600:
                pokemons = [round_opponent.pk1_opponent,
                            round_opponent.pk2_opponent, round_opponent.pk3_opponent]
                result = battleRunning(current_id, pokemons)
                round_opponent.winner = result
                round_opponent.save()

                return redirect('home')
            if (sum_pk11 + sum_pk21 + sum_pk31) > 600:
                message = "ERROR: PKNs you selected sum more than 600 points, please choose again"
                return render(request, 'battle/round_new2.html', {'form_round2': form_round2,
                                                                 'battle': battle_info, 'message': message})
    else:
        form_round2 = RoundForm2()
    return render(request, 'battle/round_new2.html', {'form_round2': form_round2,
                                                     'battle': battle_info})


def sumValid(pokemon):
    sum_result = pokemon["attack"] + pokemon["defense"] + pokemon["hp"]
    return sum_result


def battleRunning(poke_id, pokemons):
    battle_info = Battle.objects.get(id=poke_id)
    poke_info1_creator = get_pokemon_from_api(battle_info.pk1_creator)
    poke_info2_creator = get_pokemon_from_api(battle_info.pk2_creator)
    poke_info3_creator = get_pokemon_from_api(battle_info.pk3_creator)
    # poke_info_creator_list = [poke_info1_creator, poke_info2_creator, poke_info3_creator]
    poke_info1_opponent = get_pokemon_from_api(pokemons[0])
    poke_info2_opponent = get_pokemon_from_api(pokemons[1])
    poke_info3_opponent = get_pokemon_from_api(pokemons[2])

    round_one = [poke_info1_creator, poke_info1_opponent]
    round_two = [poke_info2_creator, poke_info2_opponent]
    round_three = [poke_info3_creator, poke_info3_opponent]

    winner = "nobody"
    opponent = 0
    creator = 0

    battle_rounds = [round_one, round_two, round_three]

    for battle_round in battle_rounds:
        result = roundRunning(battle_round)
        if result == "creator":
            creator = creator + 1
        else:
            opponent = opponent + 1

    if creator > opponent:
        winner = "creator"
    elif creator < opponent:
        winner = "opponent"
    else:
        winner = "creator"

    return winner
