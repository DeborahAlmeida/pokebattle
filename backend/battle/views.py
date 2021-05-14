from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from .models import Battle, Team, PokemonTeam
# from django.views.decorators.http import require_POST
# import requests
# from django.shortcuts import redirect
# from .models import Battle
# from .forms import BattleForm, RoundForm, RoundForm2
# from .battles.battle import battleRunning, message_error
# from pokemon.helpers import get_pokemon_from_api
# from .battles.base_stats import get_total_point_pokemon


class Home(TemplateView):
    template_name = 'battle/home.html'


class Invite(TemplateView):
    template_name = 'battle/invite.html'


class BattleView(CreateView):
    model = Battle
    fields = ['creator', 'opponent']
    # success_url = '/invite'

    def form_valid(self, form):
        self.object = form.save()
        Team.objects.create(battle=form.instance, trainer=self.request.user)
        return HttpResponseRedirect('/battle/pokemon')


class PokemonTeamView(CreateView):
    template_name = "battle/pokemon_form.html"
    model = PokemonTeam
    fields = ['team', 'pokemon', 'order']

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect('/battle/pokemon')

# def team(request):
#     user = Battle.objects.all()
#     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> user", user)
#     model = Team(battle_id=1, trainer_id=1)
#     model.save()
    # form.battle = battle_info.pk
    # if form.is_valid():
    #     form.save()
    # print(">>>>>>hello", user)
#     return True

# class RoundNewCreator(View):
#     form_class = RoundForm
#     initial = {'key' : 'value'}
#     template_name = 'battle/round_new.html'

#     def get(self, request, *args, **kwargs):
#         form_round = self.form_class(initial = self.initial)
#         return render(request, self.template_name, {'form_round': form_round})


#     def post(self, request, *args, **kwargs):
#         form_round = self.form_class(request.POST)
#         if form_round.is_valid():
#             round_battle = form_round.save(commit=False)
#             data_pokemons = [
#                 round_battle.pk1_creator,
#                 round_battle.pk2_creator,
#                 round_battle.pk3_creator
#             ]
#             info = get_total_point_pokemon(data_pokemons)
#             if info == True:
#                 round_battle.save()
#                 return HttpResponseRedirect('/invite/')
#             else:
#                 error = message_error()
#                 return render(request, self.template_name, {'form_round': form_round,
#                                                              'message': error})


# class RoundNewOponnent(View):
#     form_class = RoundForm2
#     initial = {'key': 'value'}
#     template_name = 'battle/round_new2.html'
#     battle_info = Battle.objects.latest('id')

#     def get(self, request, *args, **kwargs):
#             form_round2 = self.form_class(initial = self.initial)
#             battle_get = self.battle_info
#             return render(request, self.template_name, {'form_round2': form_round2,
#                                                         'battle': battle_get})

#     def post(self, request, *args, **kwargs):
#             battle = self.battle_info
#             form_round2 = self.form_class(request.POST, instance = battle)
#             if form_round2.is_valid():
#                 round_opponent = form_round2.save(commit=False)
#                 data_pokemons = [
#                     round_opponent.pk1_opponent,
#                     round_opponent.pk2_opponent,
#                     round_opponent.pk3_opponent
#                 ]
#                 info = get_total_point_pokemon(data_pokemons)
#                 current_id = battle.id
#                 if info == True:
#                     pokemons = [round_opponent.pk1_opponent,
#                                 round_opponent.pk2_opponent, round_opponent.pk3_opponent]
#                     result = battleRunning(current_id, pokemons)
#                     round_opponent.winner = result
#                     round_opponent.save()
#                     #result_battle()

#                     return HttpResponseRedirect('/')
#                 else:
#                     error = message_error()
#                     return render(request, self.template_name,
#                                 {'battle': battle_info, 'message': error})


# class Invite(View):
#     template_name = 'battle/invite.html'

#     def get(self, request):
#         return render(request, self.template_name)


# class Opponent(View):
#     template_name = 'battle/opponent.html'

#     def get(self, request):
#         return render(request, self.template_name)
