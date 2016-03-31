# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django import forms
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils.safestring import mark_safe


class SKDCropWidgetBase(forms.widgets.TextInput):

    class Media:
        js = ('skd_crop/js/skd_crop.js',)

    def __init__(self, *args, **kwargs):
        self.sizes = kwargs.pop('sizes', [])
        self.image_field = kwargs.pop('image_field', None)
        self.field_name = kwargs.pop('field_name', None)
        super(SKDCropWidgetBase, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        _template = 'skd_crop/widget2.html'
        _input = """
        <input name="{field_name}" id="id_{field_name}"
        value='{value}' class="django_skd_crop-input"/>
        """.format(
            field_name=self.field_name,
            value=value)

        context = {
            'image_field': self.image_field,
            'sizes': self.sizes,
            'input': _input}

        return mark_safe(render_to_string(_template, context=context))


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
