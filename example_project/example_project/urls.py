from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from accounts.views import ProfileCreateView, ProfileUpdateView, \
    UserProfileCreateView, UserProfileUpdateView

urlpatterns = [
    url(r'^$', ProfileCreateView.as_view(), name='profile-create'),
    url(r'^edit/(?P<pk>\d+)$', ProfileUpdateView.as_view(), name='profile-update'),
    url(r'^admin/', admin.site.urls),
    url(r'^skd-crop/', include('skd_crop.urls')),

    url(r'^users/add/$', UserProfileCreateView.as_view(),
        name='user_profile_create'),
    url(r'^users/(?P<pk>\d+)/update/$', UserProfileUpdateView.as_view(),
        name='user_profile_update'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
