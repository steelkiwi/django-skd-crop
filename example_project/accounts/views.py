# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.generic import UpdateView, CreateView

from .forms import UserProfileForm
from .models import Profile


class UserProfileView(UpdateView):
    form_class = UserProfileForm
    template_name = 'accounts/user_profile.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form = UserProfileForm(data=self.request.POST, files=self.request.FILES)
        form.save()
        if self.request.is_ajax():
            obj = get_user_model().objects.get(pk=1)
            serialized_obj = {}
            serialized_obj['pk'] = obj.pk
            serialized_obj['first_name'] = obj.first_name
            serialized_obj['last_name'] = obj.last_name
            serialized_obj['userpic_img'] = str(obj.userpic_img)
            if obj.userpic:
                serialized_obj['userpic'] = json.loads(obj.userpic)
            return JsonResponse(serialized_obj)
        else:
            return super(UserProfileView, self).form_valid(form)


class ProfileCreateView(CreateView):
    model = Profile
    fields = ['image']

    def get_success_url(self):
        return reverse('profile-update', kwargs={'pk': self.object.pk})


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['image']

    def get_success_url(self):
        return reverse('profile-update', kwargs={'pk': self.object.pk})
