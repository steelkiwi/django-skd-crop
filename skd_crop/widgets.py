# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


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
