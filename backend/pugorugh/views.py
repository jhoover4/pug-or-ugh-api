from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from . import models
from . import serializers


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'dog': reverse('dog-detail', request=request, format=format),
        'dogs': reverse('dog-list', request=request, format=format)
    })


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class DogDetailCustomView(RetrieveUpdateAPIView):
    """Allow creation and deletion of dogs on site."""

    http_method_names = ['get', 'put']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()

    def get_status(self):
        status = None

        try:
            status_provided = self.kwargs.get('status').lower()
        except AttributeError:
            raise Http404

        for choice in models.UserDog.STATUS_CHOICES:
            if choice[1].lower() == status_provided:
                status = choice[0]

        return status

    def get_queryset(self):
        """Return a queryset based on dog pk and the user dog's status."""

        return self.queryset.filter(id__gt=self.kwargs.get('pk'), userdog__status=self.get_status())

    def get_object(self):
        """Return the first dog in the queryset or a 404 if none is found."""

        dog = self.get_queryset().first()
        if not dog:
            raise Http404

        return dog

    def get_serializer_class(self):
        """Grab the user dog serializer if put is being used."""

        if self.request.method == 'PUT':
            return serializers.UserDogSerializer
        return self.serializer_class

    def perform_update(self, serializer):
        """Update used for PUT request."""

        serializer.save(status=self.get_status())


class DogDetailDeleteView(DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()


class DogListView(ListCreateAPIView):
    """Allow creation and deletion of dogs on site."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer


class UserPrefView(RetrieveUpdateAPIView, CreateModelMixin):
    """Create, update, or view user preferences."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer
