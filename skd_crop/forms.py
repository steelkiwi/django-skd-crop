# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django import forms


class ImageForm(forms.Form):
    image = forms.FileField()
