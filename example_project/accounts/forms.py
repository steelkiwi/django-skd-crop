# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms import formset_factory

from accounts.models import UserProfile, Profile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'first_name',
            'last_name',
            'userpic_img',
            'userpic',
        )
