# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
from mimetypes import guess_type

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import Http404, JsonResponse
from django.utils.datastructures import MultiValueDict
from django.views.decorators.http import require_POST
from django.views.generic import FormView
from easy_thumbnails.files import get_thumbnailer, get_image_dimensions

from .forms import ImageForm, TmpSourceForm


class UploadView(FormView):
    form_class = ImageForm

    def form_valid(self, form):
        if self.request.is_ajax():
            resize_source = form.cleaned_data.get('resize_source')
            image = form.cleaned_data['image']
            upload_to = form.cleaned_data['upload_to']
            filename = os.path.join(upload_to, image.name)
            thumbnailer = get_thumbnailer(image, relative_name=filename)
            if resize_source:
                resize_source = json.loads(resize_source)
            else:
                resize_source = {'size': get_image_dimensions(thumbnailer)}
            source_image = thumbnailer.get_thumbnail(resize_source)
            source_image.open()
            source_file = InMemoryUploadedFile(
                    file=source_image.file,
                    field_name='image',
                    name=source_image.name,
                    content_type=guess_type(source_image.name)[0],
                    size=source_image.size,
                    charset=None)
            files = MultiValueDict({'image': [source_file]})
            tmp_form = TmpSourceForm(data=None, files=files, resize_source=resize_source)
            if tmp_form.is_valid():
                tmp_source = tmp_form.save()
                source_image.storage.delete(source_image.name)
                return JsonResponse({'url': tmp_source.image.url, 'pk': tmp_source.id})
            else:
                return JsonResponse({'error': 'error'}, status=400)

        else:
            raise Http404

upload = require_POST(UploadView.as_view())
