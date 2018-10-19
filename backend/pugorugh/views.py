from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import permissions
from rest_framework import status as drf_status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, \
    DestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

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


class DogDetailUpdateView(APIView):
    def put(self, request, pk, status, format=None):
        for choice in models.UserDog.STATUS_CHOICES:
            if choice[1].lower() == status:
                status = choice[0]
            else:
                status = None

        serializer = serializers.UserDogSerializer(data={'user': self.request.user.id, 'dog': pk, 'status': status})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=drf_status.HTTP_200_OK)
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)


class DogGetNextView(RetrieveAPIView):
    """Allow creation and deletion of dogs on site."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()

    def get_status(self):
        status = None

        try:
            status_provided = self.kwargs.get('status').lower()
        except AttributeError:
            raise ValidationError('Status was incorrect. Must be liked, disliked, or undecided.')
        else:
            if status_provided not in ['liked', 'disliked', 'undecided']:
                raise ValidationError('Status was incorrect. Must be liked, disliked, or undecided.')

        for choice in models.UserDog.STATUS_CHOICES:
            if choice[1].lower() == status_provided:
                status = choice[0]

        return status

    def get_queryset(self):
        """Return a queryset based on dog pk and the user dog's status."""

        return self.queryset.filter(id__gt=self.kwargs.get('pk'), userdog__status=self.get_status())

    def get_object(self):
        """Return the first dog in the queryset or a 404 if none is found."""

        queryset = self.get_queryset()

        if len(queryset) == 1:
            dog = queryset[0]
        else:
            dog = self.get_queryset().first()

        if not dog:
            raise Http404

        return dog


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

    lookup_field = None

    def get_object(self):
        user = self.request.user

        try:
            user_pref = models.UserPref.objects.get(user_id=user.id)
        except models.UserPref.DoesNotExist:
            user_pref = models.UserPref.objects.create(user=user)

        return user_pref
