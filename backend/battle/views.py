from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from .models import Battle, Team
from django.urls import reverse_lazy
from .forms import TeamForm, BattleForm


class Home(TemplateView):
    template_name = 'battle/home.html'


class Invite(TemplateView):
    template_name = 'battle/invite.html'


class BattleView(CreateView):
    model = Battle
    form_class = BattleForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return HttpResponseRedirect(reverse_lazy("team_create", args=(form.instance.id,)))


class TeamView(CreateView):
    model = Team
    template_name = "battle/pokemon_form.html"
    form_class = TeamForm
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        self.object = None
        battle_id = kwargs['pk']
        battle_object = Battle.objects.get(pk=battle_id)
        Team.objects.create(battle=battle_object, trainer=battle_object.creator)
        Team.objects.create(battle=battle_object, trainer=battle_object.opponent)
        return super().get(request, *args, **kwargs)
