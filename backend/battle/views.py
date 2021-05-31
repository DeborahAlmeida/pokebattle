from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from .models import Battle, Team
from django.urls import reverse_lazy
from .forms import TeamForm, BattleForm


class Home(TemplateView):
    template_name = 'battle/home.html'


class Invite(TemplateView):
    template_name = 'battle/invite.html'



class BattleView(CreateView):
    model = Battle
    template_name = 'battle/battle_form.html'
    form_class = BattleForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return HttpResponseRedirect(reverse_lazy("team_create", args=(form.instance.id, 1, )))


class TeamView(CreateView):
    model = Team
    template_name = "battle/pokemon_form.html"
    form_class = TeamForm
    success_url = reverse_lazy("invite")

    def get_initial(self):
        super(TeamView, self).get_initial()
        self.initial = {"battle": self.kwargs['pk'], "user": self.kwargs['user']}
        return self.initial

    def get_success_url(self):
        if self.initial['user'] == 1:
            return str(self.success_url)
        return reverse_lazy('home')


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
