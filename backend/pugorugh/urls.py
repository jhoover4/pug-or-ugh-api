from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh.views import UserRegisterView, DogDetailUpdateView, DogListView, api_root, DogDetailDeleteView, \
    DogGetNextView, UserPrefView

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/$', api_root, name='api-root'),
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),
    url(r'^api/user/preferences/$', UserPrefView.as_view(), name='preferences-user'),
    url(r'^api/dog/(?P<pk>\d+)/(?P<status>[\w\-]+)/$', DogDetailUpdateView.as_view(),
        name='dog-detail-custom'),
    url(r'^api/dog/(?P<pk>-?\d+)/(?P<status>[\w\-]+)/next/$', DogGetNextView.as_view(),
        name='dog-detail-next'),
    url(r'^api/dog/(?P<pk>\d+)/$', DogDetailDeleteView.as_view(), name='dog-detail-delete'),
    url(r'^api/dogs/$', DogListView.as_view(), name='dog-list'),
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html'))
])
