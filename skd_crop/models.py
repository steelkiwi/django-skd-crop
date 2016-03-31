# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ungettext
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer

from skd_crop.widgets import SKDCropWidgetBase


def parse_sizes(value):
    return SKDImage(sizes=value)


def str_json_to_dict(value):
    return json.loads(str(value))


@python_2_unicode_compatible
class SKDImage(object):
    """
    Object with sizes for cropping images.
    """

    def __init__(self, sizes=None):
        """
        :param sizes (dict):
        """
        self.sizes = sizes

    def __str__(self):
        return str(self.sizes)


class SKDImageField(models.Field):
    """
    Data for cropping images.
    """
    description = "Sizes for cropping images."

    def __init__(self, image_field=None, sizes=None, upload_to=None, *args, **kwargs):
        kwargs['max_length'] = 500
        self.image_field = image_field
        self.sizes = sizes
        self.upload_to = upload_to
        super(SKDImageField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(SKDImageField, self).deconstruct()
        return name, path, args, kwargs

    def db_type(self, connection):
        """
        Chose the database field.
        """
        return 'char(%s)' % self.max_length

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return parse_sizes(value)

    def to_python(self, value):
        if isinstance(value, SKDImage):
            return value

        if value is None:
            return value

        return parse_sizes(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        return str(value)

    def formfield(self, **kwargs):
        defaults = {'widget': SKDCropWidgetBase(
            image_field=self.image_field,
            sizes=self.sizes,
            field_name=self.name)}
        defaults.update(kwargs)
        return super(SKDImageField, self).formfield(**defaults)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def validate(self, value, model_instance):
        super(SKDImageField, self).validate(value, model_instance)

        # TODO: add check for duplicate keys
        # TODO: add check for sizes
        # TODO: add check for all keys

        try:
            undefined_items = set(json.loads(str(value)).keys()) - set(self.sizes.keys())
        except ValueError:
            undefined_items = None

        if undefined_items:
            count = len(undefined_items)
            msg = ungettext(
                'is not valid item.',
                'is not valid items.',
                count)

            raise ValidationError("{items} {msg}".format(
                items=', '.join('`%s`' % i for i in undefined_items),
                msg=msg))

    def pre_save(self, model_instance, add):
        # TODO: Add here functionality for generating cropped images.
        image = getattr(model_instance, self.image_field)

        thumbnailer = get_thumbnailer(image)
        thumbnail_options = {'crop': True}

        for size in (50, 100, 250):
            thumbnail_options.update({'size': (size, size)})
            thumbnailer.get_thumbnail(thumbnail_options)

        return super(SKDImageField, self).pre_save(model_instance, add)


class TmpSource(models.Model):
    image = ThumbnailerImageField(upload_to='tmp')
    created = models.DateTimeField(auto_now=True)
