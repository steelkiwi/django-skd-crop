# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django import forms
from easy_thumbnails.fields import ThumbnailerImageField

from .widgets import SKDMultiWidgetBasic, SKDCropWidget


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


class SKDThumbnailerImageModelField(ThumbnailerImageField):

    def __init__(self, *args, **kwargs):
        self.sizes = kwargs.pop('sizes', None)
        super(SKDThumbnailerImageModelField, self).__init__(*args, **kwargs)
        self.widget = SKDCropWidget(
            sizes=self.sizes,
            upload_to=self.upload_to,
            resize_source=json.dumps(self.resize_source)
        )

    def formfield(self, **kwargs):
        defaults = {'widget': self.widget}
        defaults.update(kwargs)
        return super(SKDThumbnailerImageModelField, self).formfield(**defaults)
