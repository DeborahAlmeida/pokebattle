from rest_framework import serializers
from battle.models import Battle
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import PasswordResetForm
from battle.battles.email import send_invite_email

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    # this serializer is used to return an object instead of
    # an id whenever it's used as a form field
    class Meta:
        model = User
        fields = ("email", "id")


class BattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ("id", "creator", "opponent", "winner")


class BattleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ("id", "creator", "opponent", "winner")

    def validate_creator(self, value):
        if self.initial_data['creator'] == self.initial_data['opponent']:
            raise serializers.ValidationError("ERROR: You can't challenge yourself.")
        return value

    def validate_opponent(self, value):
        if 'opponent' not in self.initial_data:
            raise serializers.ValidationError("ERROR: You need to choose an opponent")

        opponent_email = self.initial_data["opponent"]

        try:
            value = User.objects.get(email=opponent_email)
            value.is_guest = False
        except User.DoesNotExist:
            value = User.objects.create(email=opponent_email)
            value.is_guest = True
            random_password = get_random_string(length=64)
            value.set_password(random_password)
            value.save()
        return value

    def create(self, validated_data):
        opponent = self.initial_data["opponent"]
        if validated_data['opponent'].is_guest:
            invite_form = PasswordResetForm(data={"email": opponent.email})
            invite_form.is_valid()
            invite_form.save(
                self, subject_template_name='registration/guest_email_subject.txt',
                email_template_name='registration/guest_email.html',
                from_email=settings.FROM_EMAIL,)
        else:
            send_invite_email(validated_data['opponent'], validated_data['creator'])
        return Battle.objects.create(**validated_data)

