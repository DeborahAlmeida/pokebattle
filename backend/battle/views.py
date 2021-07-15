from django.http import HttpResponseRedirect
from django.db.models import Q
from django.conf import settings
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import (
    SetPasswordForm,
)
from django.contrib.auth import (
    get_user_model, login as auth_login,
)
from django.utils.http import (
    urlsafe_base64_decode,
)
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.views.generic.edit import FormView
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.shortcuts import resolve_url


from battle.models import Battle, Team
from battle.forms import TeamForm, BattleForm, UserForm
from battle.battles.base_stats import get_pokemons_team
from battle.tasks import run_battle_and_send_result_email

from users.models import User

from pokemon.models import Pokemon

UserModel = get_user_model()
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


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


class PasswordCreateConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_create_confirm.html'
    title = ('Create a password')
    token_generator = default_token_generator

    def __init__(self, **kwargs):
        self.validlink = None
        self.user = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if 'uidb64' not in kwargs or 'token' not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        """
        :type other: PasswordCreateConfirmView
        :rtype PasswordCreateConfirmView:
        """

        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)  # pylint: disable=protected-access

        except (
            TypeError,
            ValueError,
            OverflowError,
            UserModel.DoesNotExist,
                ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': ('Password create unsuccessful'),
                'validlink': False,
            })
        return context


class PasswordCreateCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_create_complete.html'
    title = ('Password create complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context
