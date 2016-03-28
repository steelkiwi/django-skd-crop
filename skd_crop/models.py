# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.db import models
from django.forms import CharField
from easy_thumbnails.fields import ThumbnailerImageField

"""
Создать SKDImageFormField (кастомное поле формы со своим виджетом)
'coordinates': {
    'top_left': "0.5x0.5;",
    'top_right': "0.5x0.8;",
    'bottom_left': "0.3x0.5;",
    'bottom_right': "0.3x0.8;",
}
DATA IN FIELD IN DATABASE:
{
    "userpic_l": {
        "cropped_image": "/media/images/cache/new_userpic_l_1234.jpg",
        "coordinates": {
            "top_left": "0.5x0.5",
            "top_right": "0.5x0.8",
            "bottom_left": "0.3x0.5",
            "bottom_right": "0.3x0.8"
        }
    },
    "userpic_s": {
        "cropped_image": "/media/images/cache/new_userpic_s_1234.jpg",
        "coordinates": {
            "top_left": "0.5x0.5",
            "top_right": "0.5x0.8",
            "bottom_left": "0.3x0.5",
            "bottom_right": "0.3x0.8"
        }
    }
}
"""

def parse_value(value):
    """Parse value parameters"""
    cropped_images = json.loads(value)
    # raise ValidationError("Invalid input for a Hand instance")
    return SKDImage(parameters=cropped_images)


class SKDImage(object):
    """Object with values for cropped images"""

    def __init__(self, image_field='', parameters=''):
        self.image_field = image_field
        self.parameters = parameters

    def __str__(self):
        # self.get_list_of_parameters()
        return str(self.parameters)

    # def get_list_of_parameters(self):
    #     return parse_value(self.parameters)


class SKDImageField(models.TextField):
    """Data for cropped images"""
    description = "Parameters for cropped images."

    def __init__(self, image_field='', parameters=list(), max_length=None,
                 blank=True, verbose_name=None, help_text=None):

        if '__' in image_field:
            self.image_field, self.image_fk_field = image_field.split('__')
        else:
            self.image_field, self.image_fk_field = image_field, None

        self.parameters = parameters
        field_kwargs = {
            'default': '',
            'blank': blank,
            'max_length': max_length,
            'verbose_name': verbose_name,
            'help_text': help_text
        }

        # print('__init__ kwargs:', field_kwargs)

        super(SKDImageField, self).__init__(**field_kwargs)

    def deconstruct(self):
        if self.image_fk_field:
            image_field = '%s__%s' % (self.image_field, self.image_fk_field)
        else:
            image_field = self.image_field

        # print('deconstruct:', image_field)

        args = ()
        kwargs = {
            'image_field': image_field,
            'parameters': self.parameters,
            'verbose_name': self.verbose_name,
            'help_text': self.help_text,
            'max_length': self.max_length,
        }
        return self.name, 'skd_crop.models.SKDImageField', args, kwargs

    # def contribute_to_class(self, cls, name):
    #     super(SKDImageField, self).contribute_to_class(cls, name)
    #     if not cls._meta.abstract:
    #         # attach a list of fields that are referenced by the ImageRatioField
    #         # so we can set the correct widget in the ModelAdmin
    #         if not hasattr(cls, 'crop_fields'):
    #             cls.add_to_class('crop_fields', {})
    #         cls.crop_fields[self.image_field] = {
    #             'fk_field': self.image_fk_field,
    #         }
    #         # attach ratiofields to cls
    #         if not hasattr(cls, 'ratio_fields'):
    #             cls.add_to_class('ratio_fields', [])
    #         cls.ratio_fields.append(name)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return value

    def to_python(self, value):
        if isinstance(value, SKDImage):
            return value
        if value is None:
            return value
        return value

    # def get_prep_value(self, value):
    #     return ''.join([''.join(l) for l in (value.image_field,
    #                                          value.parameters)])

    # def get_db_prep_value(self, value, connection, prepared=False):
    #     value = super(BinaryField, self).get_db_prep_value(
    #         value, connection, prepared)
    #     if value is not None:
    #         return connection.Database.Binary(value)
    #     return value

    # def get_internal_type(self):
    #     return 'CharField'

    # def value_to_string(self, obj):
    #     print('*'*500, self, obj, '*'*500)
    #     value = self._get_val_from_obj(obj)
    #     return self.get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': CharField}
        defaults.update(kwargs)
        return super(SKDImageField, self).formfield(**defaults)


class TmpSource(models.Model):
    image = ThumbnailerImageField(upload_to='tmp')
    created = models.DateTimeField(auto_now=True)
