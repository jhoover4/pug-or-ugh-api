from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh.views import api_root, DogDetailDeleteView, DogDetailUpdateView, DogGetNextView, DogListView, \
    DogStatusListView, UserRegisterView, UserPrefView

# API endpoints
urlpatterns = format_suffix_patterns([
    path('api/', api_root, name='api-root'),
    path('api/user/login/', obtain_auth_token, name='login-user'),
    path('api/user/', UserRegisterView.as_view(), name='register-user'),
    path('api/user/preferences/', UserPrefView.as_view(), name='preferences-user'),
    re_path(r'^api/dog/(?P<pk>\d+)/(?P<status>[\w\-]+)/$', DogDetailUpdateView.as_view(),
        name='dog-detail-custom'),
    re_path(r'^api/dog/(?P<pk>-?\d+)/(?P<status>[\w\-]+)/next/$', DogGetNextView.as_view(),
        name='dog-detail-next'),
    re_path(r'^api/dog/(?P<pk>\d+)/$', DogDetailDeleteView.as_view(), name='dog-detail-delete'),
    path('api/dogs/', DogListView.as_view(), name='dog-list'),
    re_path(r'^api/dogs/(?P<status>[\w\-]+)/$', DogStatusListView.as_view(),
        name='dog-status-list'),
    re_path(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    path('', TemplateView.as_view(template_name='index.html'))
])
