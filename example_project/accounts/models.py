# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cropduster.fields import CropDusterField
from cropduster.resizing import Size
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from skd_crop.fields import SKDThumbnailerImageModelField
from skd_crop.models import SKDImageField


class UserProfile(AbstractUser):
    userpic_img = models.ImageField(blank=True, upload_to='images/userpics/')
    userpic = SKDImageField(
        verbose_name=_('userpic'),
        help_text=_('This is help text from field.'),
        max_length=5000,

        image_field='userpic_img',  # link to field pk with original image
        parameters={
            'userpic_l': {
                'title': _("Large Userpic"),
                'ratio': "1:1",  # n:n, None. This field have
                'size': "512x512",  # n:n max width x height (in px)
            },
            'userpic_s': {
                'title': _("Small Userpic"),
                'ratio': "3:1",  # n:n, None. This field have
                'size': "x224",  # n:n max width x height (in px)
            },
            'userpic_custom_crop': {
                'title': _("Custom cropped Userpic"),
                'size': "224x224",  # n:n max width x height (in px)
            },
            'userpic_error_ratio': {
                'title': _("Large Userpic"),
                'ratio': "3:1",  # n:n, None. This field have
                'size': "228x228",  # n:n max width x height (in px)
            }
        },
    )

    def __unicode__(self):
        return 'UserProfile %s' % self.username


class ChildProfile(models.Model):
    name = models.CharField(max_length=50)
    avatar = CropDusterField(upload_to='img/avatars', sizes=[
        Size('main', w=1024, h=768, label='Main'),
        Size('thumb', w=400, h=300, label='Thumbnail'),
    ])


class Profile(models.Model):
    IMAGE_SIZES = {
        'large': {'size': (800, 600), 'crop': True, 'label': _('Large')},
        'medium': {'size': (500, 300), 'crop': True, 'label': _('Medium')},
        'small': {'size': (200, 100), 'crop': True, 'label': _('Small')}
    }
    image = SKDThumbnailerImageModelField(upload_to='avatars', resize_source={'size': (1024, 768)}, sizes=IMAGE_SIZES)
