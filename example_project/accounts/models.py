# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from skd_crop.fields import SKDThumbnailerImageModelField

from skd_crop.models import SKDImageField


class UserProfile(models.Model):
    name = models.CharField(max_length=50)
    userpic_img = models.ImageField(blank=True, upload_to='images/userpics/')
    userpic = SKDImageField(
        blank=True,
        upload_to='images/userpics/tmp/',
        image_field='userpic_img',
        sizes={
            'large': {
                'label': _("Large"),
                'width': 400,
                'height': 400
            },
            'small': {
                'label': _("Small"),
                'width': 50,
                'height': 50
            },
        },
    )

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    IMAGE_SIZES = {
        'large': {'size': (800, 600), 'crop': True, 'label': _('Large')},
        'medium': {'size': (500, 300), 'crop': True, 'label': _('Medium')},
        'small': {'size': (200, 100), 'crop': True, 'label': _('Small')}
    }
    image = SKDThumbnailerImageModelField(upload_to='avatars', resize_source={'size': (600, 450)}, sizes=IMAGE_SIZES)
    name = models.CharField(max_length=50, blank=True)
