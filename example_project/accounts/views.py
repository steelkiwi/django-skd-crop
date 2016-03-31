# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import UpdateView, CreateView

from .models import Profile, UserProfile


class UserProfileCreateView(CreateView):
    model = UserProfile
    fields = '__all__'
    template_name = 'accounts/user_profile.html'
    success_url = reverse_lazy('user_profile_create')

    def get_success_url(self):
        return reverse('user_profile_update', kwargs={'pk': self.object.pk})


class UserProfileUpdateView(UserProfileCreateView, UpdateView):
    context_object_name = 'object'


class ProfileCreateView(CreateView):
    model = Profile
    fields = ['image', 'name']

    def get_success_url(self):
        return reverse('profile-update', kwargs={'pk': self.object.pk})


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['image', 'name']

    def get_success_url(self):
        return reverse('profile-update', kwargs={'pk': self.object.pk})
