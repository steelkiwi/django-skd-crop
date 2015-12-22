# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django import forms
from django.forms.widgets import CheckboxInput
from django.template.loader import render_to_string
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


class SKDMultiWidgetBasic(forms.widgets.MultiWidget):

    def __init__(self):
        widgets = (
            forms.TextInput(),
            forms.TextInput(),
            forms.TextInput(),
            forms.TextInput(),
            forms.TextInput(),
        )
        super(SKDMultiWidgetBasic, self).__init__(widgets)

    def decompress(self, value):
        if value:
            value = value.get_list_of_parameters()
            return [
                value['userpic_l']['cropped_image'],
                value['userpic_l']['coordinates']['top_left'],
                value['userpic_l']['coordinates']['top_right'],
                value['userpic_l']['coordinates']['bottom_left'],
                value['userpic_l']['coordinates']['bottom_right'],
            ]
        return ['', '']


class SKDCropWidget(forms.widgets.FileInput):

    def __init__(self, attrs=None, **kwargs):
        self.sizes = kwargs.pop('sizes', [])
        self.upload_to = kwargs.pop('upload_to', '')
        super(SKDCropWidget, self).__init__(attrs)

    def is_initial(self, value):
        return bool(value and hasattr(value, 'url'))

    def render(self, name, value, attrs=None):
        template = 'skd_crop/widget.html'
        context = {
            'upload_to': self.upload_to,
            'sizes': self.sizes,
            'tmp_upload_to': os.path.join('tmp', self.upload_to),
        }
        if self.is_initial(value):
            context['is_initial'] = True
        return mark_safe(render_to_string(template, context=context))
