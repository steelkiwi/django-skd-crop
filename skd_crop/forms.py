# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django import forms

from skd_crop.models import TmpSource


class ImageForm(forms.Form):
    image = forms.FileField()
    upload_to = forms.CharField(required=False)
    resize_source = forms.CharField(required=False)


class TmpSourceForm(forms.ModelForm):

    class Meta:
        model = TmpSource
        fields = ['image']

    def __init__(self, *args, **kwargs):
        self.resize_source = kwargs.pop('resize_source')
        super(TmpSourceForm, self).__init__(*args, **kwargs)
        self.fields['image'].resize_source = self.resize_source

