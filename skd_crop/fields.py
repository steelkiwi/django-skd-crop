# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from easy_thumbnails.fields import ThumbnailerImageField

from .widgets import SKDCropWidget


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
