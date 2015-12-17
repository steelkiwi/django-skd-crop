# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from skd_crop.widgets import SKDMultiWidgetBasic


class SKDMultiField(forms.MultiValueField):
    widget = SKDMultiWidgetBasic

    def __init__(self, *args, **kwargs):
        fields = (
            forms.CharField(),
            forms.CharField(),
            forms.CharField(),
        )
        super(SKDMultiField, self).__init__(fields, *args)

    def compress(self, data_list):
        if data_list:
            return ':::'.join(data_list)
        return ''
