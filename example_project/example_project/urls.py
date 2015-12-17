from django.conf.urls import url
from django.contrib import admin

from accounts.views import UserProfileView


urlpatterns = [
    url(r'^$', UserProfileView.as_view(), name='user_profile'),
    url(r'^admin/', admin.site.urls),
]
