from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.conf import settings
from urllib.parse import urljoin
import requests

from battle.models import Battle, Team
from battle.forms import TeamForm, BattleForm, UserForm
from battle.battles.battle import run_battle, set_winner
from battle.battles.email import send_invite_email
from django.utils.html import format_html


from users.models import User

from pokemon.models import Pokemon

from dal import autocomplete


class Home(TemplateView):
    template_name = 'battle/home.html'


class Invite(TemplateView):
    template_name = 'battle/invite.html'


class BattleView(CreateView):
    model = Battle
    template_name = 'battle/battle_form.html'
    form_class = BattleForm

    def get_initial(self):
        obj_creator = self.request.user
        self.initial = {"creator": obj_creator}
        return self.initial

    def form_valid(self, form):
        form.save()
        send_invite_email(form.instance.opponent, form.instance.creator)
        return HttpResponseRedirect(reverse_lazy("team_create", args=(form.instance.id, )))


class TeamView(CreateView):
    model = Team
    template_name = "battle/pokemon_form.html"
    form_class = TeamForm
    success_url = reverse_lazy("invite")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_trainer = self.request.user
        pokemons = Pokemon.objects.all()

        context['pokemons'] = pokemons
        context['battle'] = self.kwargs['pk']
        context['trainer'] = obj_trainer
        return context

    def form_valid(self, form):
        team = form.save()
        if team.battle.teams.count() == 2:
            team_winner = run_battle(team.battle)
            set_winner(team_winner.trainer, team.battle)
            return HttpResponseRedirect(reverse_lazy("home"))

        return HttpResponseRedirect(reverse_lazy("invite"))


class BattleList(ListView):
    model = Battle

    def get_queryset(self):
        queryset = Battle.objects.filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        )
        return queryset


class BattleDetail(DetailView):
    model = Battle
    template_name = "battle/battle_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(battle=self.object, trainer=self.request.user)
        context['team'] = team
        return context


class BattleSignUp(CreateView):
    model = User
    form_class = UserForm
    template_name = "battle/user/signup_form.html"
    success_url = reverse_lazy("signup_sucess")


class SignUpSucess(TemplateView):
    template_name = "battle/user/sucess_signup.html"


class PokemonAutocomplete(autocomplete.Select2QuerySetView):
    template_name = "battle/teste.html"
    def get_queryset(self):
        qs = Pokemon.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def get_result_label(self, result):
        return format_html('{}', result.name)

    def get_selected_result_label(self, result):
        return result.name
