# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django import forms
from django.forms.widgets import CheckboxInput
from django.template.loader import render_to_string
from django.templatetags.static import static
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

    class Media:
        js = ('skd_crop/js/skd_crop.js',)

    def __init__(self, attrs=None, **kwargs):
        self.sizes = kwargs.pop('sizes', [])
        self.upload_to = kwargs.pop('upload_to', '')
        self.template = kwargs.pop('template_name', 'skd_crop/widget.html')
        self.no_image = kwargs.pop('default_url', static('skd_crop/img/no_ava.png'))
        self.resize_source = kwargs.pop('resize_source', {})
        super(SKDCropWidget, self).__init__(attrs)

    def is_initial(self, value):
        return bool(value and hasattr(value, 'url'))

    def render(self, name, value, attrs=None):
        template = self.template
        context = {
            'upload_to': self.upload_to,
            'sizes': self.sizes,
            'tmp_upload_to': os.path.join('tmp', self.upload_to),
            'name': name,
            'resize_source': self.resize_source,
        }
        if self.is_initial(value):
            context['initial'] = True
            context['img_src'] = value.url
        else:
            context['img_src'] = self.no_image
        return mark_safe(render_to_string(template, context=context))
