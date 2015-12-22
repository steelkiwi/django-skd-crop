from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from accounts.views import UserProfileView, ProfileCreateView, ProfileUpdateView

urlpatterns = [
    url(r'^$', ProfileCreateView.as_view(), name='profile-create'),
    url(r'^edit/(?P<pk>\d+)$', ProfileUpdateView.as_view(), name='profile-update'),
    url(r'^admin/', admin.site.urls),
    url(r'^cropduster/', include('cropduster.urls')),
    url(r'^ajax/', include('skd_crop.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
