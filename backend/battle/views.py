from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

from battle.models import Battle, Team
from battle.forms import TeamForm, BattleForm, UserForm
from battle.battles.base_stats import get_pokemons_team
from battle.tasks import run_battle_and_send_result_email

from users.models import User

from pokemon.models import Pokemon


class Home(TemplateView):
    template_name = 'battle/home.html'


class Invite(LoginRequiredMixin, TemplateView):
    template_name = 'battle/invite.html'


class BattleView(LoginRequiredMixin, CreateView):
    model = Battle
    template_name = 'battle/battle_form.html'
    form_class = BattleForm

    def get_initial(self):
        obj_creator = self.request.user
        self.initial = {"creator": obj_creator}
        return self.initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        context['users'] = users
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy("team_create", args=(form.instance.id, )))


class TeamView(LoginRequiredMixin, CreateView):
    model = Team
    template_name = "battle/pokemon_form.html"
    form_class = TeamForm
    success_url = reverse_lazy("invite")

    def get_initial(self):
        initial = {"battle": self.kwargs['pk'], "trainer": self.request.user.id}
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pokemons = Pokemon.objects.all()
        context['pokemons'] = pokemons
        return context

    def form_valid(self, form):
        team = form.save()
        if team.battle.teams.count() == 2:
            run_battle_and_send_result_email.delay(team.battle.id)
            return HttpResponseRedirect(reverse_lazy("home"))

        return HttpResponseRedirect(reverse_lazy("invite"))


class BattleList(LoginRequiredMixin, ListView):
    model = Battle

    def get_queryset(self):
        queryset = Battle.objects.filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        ).order_by('-id')
        return queryset


class BattleDetail(LoginRequiredMixin, DetailView):
    model = Battle
    template_name = "battle/battle_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pokemons_creator = get_pokemons_team(self.object, self.object.creator)
        pokemons_opponent = get_pokemons_team(self.object, self.object.opponent)
        pokemons_user = None
        if self.object.creator == self.request.user:
            pokemons_user = pokemons_creator
        else:
            pokemons_user = pokemons_opponent
        context['pokemons_creator'] = pokemons_creator
        context['pokemons_opponent'] = pokemons_opponent
        context['pokemons_user'] = pokemons_user
        return context


class BattleSignUp(CreateView):
    model = User
    form_class = UserForm
    template_name = "battle/user/signup_form.html"
    success_url = reverse_lazy("signup_sucess")


class SignUpSucess(TemplateView):
    template_name = "battle/user/sucess_signup.html"


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordCreateConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_create_confirm.html'
    title = ('Create a password')


class PasswordCreateCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_create_complete.html'
    title = ('Password create complete')
