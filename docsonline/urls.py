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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        name='auth_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        name='auth_logout'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', 'plantillas.views.home', name='home'),
    url(r'^CreateDraft/$', 'plantillas.views.CreateDraft', name='CreateDraft'),
    url(r'^plantillas/$', 'plantillas.views.plantillas', name='plantillas'),
    url(r'^plantillas/(?P<doc_id>\w+-.)/$', 'plantillas.views.plantillas',
        name='plantillas'),
    url(r'^publicmodels/$', 'plantillas.views.publicmodels',
        name='publicmodels'),
    url(r'^publicmodels/tag/(?P<tag>\w+)/$', 'plantillas.views.tagpagePublic',
        name='tagpagepublic'),
    url(r'^misdocs/$', 'plantillas.views.mydocs',
        name='misdocs'),
    url(r'^misdocs/tag/(?P<tag>\w+)/$', 'plantillas.views.tagpagePrivate',
        name='tagpageprivate'),
    url(r'^viewdoc/(?P<doc_id>\w+-.)/$', 'plantillas.views.viewdoc',
        name='viewdoc'),
    url(r'^newdoc/(?P<doc_id>\w+-.)/$', 'plantillas.views.newdoc',
        name='newdoc'),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings',
                              app_name='ratings')),

    url(r'^summernote/', include('django_summernote.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
