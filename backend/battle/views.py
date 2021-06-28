from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from battle.models import Battle, Team
from battle.forms import TeamForm, BattleForm, UserForm
from battle.battles.battle import run_battle, set_winner

from users.models import User


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
        return HttpResponseRedirect(reverse_lazy("team_create", args=(form.instance.id, )))


class TeamView(CreateView):
    model = Team
    template_name = "battle/pokemon_form.html"
    form_class = TeamForm
    success_url = reverse_lazy("invite")

    def get_initial(self):
        obj_battle = get_object_or_404(Battle, pk=self.kwargs['pk'])
        obj_trainer = self.request.user
        self.initial = {"battle": obj_battle, "trainer": obj_trainer}
        return self.initial

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
    success_url = reverse_lazy("invite")


class SignUpSucess(TemplateView):
    template_name = "battle/user/sucess_signup.html"
