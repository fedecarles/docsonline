"""testurl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from plantillas.views import (home, CreateDraft, plantillas, publicmodels,
                              viewdoc, newdoc, update_profile, view_profile)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', auth_views.login,
        name='auth_login'),
    url(r'^accounts/logout/$', auth_views.logout,
        name='auth_logout'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', home, name='home'),
    url(r'^CreateDraft/$', CreateDraft, name='CreateDraft'),
    url(r'^plantillas/$', plantillas, name='plantillas'),
    url(r'^plantillas/(?P<doc_id>\w+-.)/$', plantillas, name='plantillas'),
    url(r'^publicmodels/$', publicmodels, name='publicmodels'),
    url(r'^publicmodels/tag/(?P<tag>\w+)/$', publicmodels, name='publicmodels'),
    url(r'^viewdoc/(?P<doc_id>\w+-.)/$', viewdoc, name='viewdoc'),
    url(r'^newdoc/(?P<doc_id>\w+-.)/$', newdoc, name='newdoc'),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings',
                              app_name='ratings')),
    url(r'^update_profile/$', update_profile, name='update_profile'),
    url(r'^view_profile/$', view_profile, name='view_profile'),
    url(r'^view_profile/(?P<id>\d+)/$', view_profile, name='view_profile'),
    url(r'^view_profile/(?P<id>\d+)/tag/(?P<tag>\w+)/$',
        view_profile, name='view_profile_tags'),


    url(r'^summernote/', include('django_summernote.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
