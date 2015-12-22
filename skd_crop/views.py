# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.views.decorators.http import require_POST
from django.views.generic import FormView

from .forms import ImageForm


class UploadView(FormView):
    form_class = ImageForm

    def form_valid(self, form):
        return super(UploadView, self).form_valid(form)

upload = require_POST(UploadView.as_view())
