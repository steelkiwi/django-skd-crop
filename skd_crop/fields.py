# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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


class SKDThumbnailerImageFormField(forms.FileField):
    # widget = forms.widgets.ClearableFileInput
    widget = SKDCropWidget


class SKDThumbnailerImageModelField(ThumbnailerImageField):

    def __init__(self, *args, **kwargs):
        self.sizes = kwargs.pop('sizes', None)
        super(SKDThumbnailerImageModelField, self).__init__(*args, **kwargs)
        self.widget = SKDCropWidget(sizes=self.sizes, upload_to=self.upload_to)

    def formfield(self, **kwargs):
        defaults = {'widget': self.widget}
        defaults.update(kwargs)
        return super(SKDThumbnailerImageModelField, self).formfield(**defaults)
