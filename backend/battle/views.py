from django.shortcuts import render
from django.shortcuts import redirect
#from .models import Gamer
from users.models import User
from .models import Gamer, Battle
from .forms import BattleForm, RoundForm, RoundForm2


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
    if request.method == "POST":
        formRound = RoundForm(request.POST)
        if formRound.is_valid():
            roundBattle = formRound.save(commit=False)
            roundBattle.save()
            return redirect('invite')
    else:
        formRound = RoundForm()
    return render(request, 'battle/round_new.html', {'formRound': formRound})

def invite(request):
    return render(request, 'battle/invite.html')

def player2(request):
    return render(request, 'battle/opponent.html')

def round_new2(request):
    battleInfo = Battle.objects.get(id=30)
    if request.method == "POST":
        formRound2 = RoundForm2(request.POST, instance=battleInfo)
        if formRound2.is_valid():
            formRound2.save()
            return redirect('home')
    else:
        formRound2 = RoundForm2()
    return render(request, 'battle/round_new2.html', {'formRound2': formRound2, 'battle':battleInfo})