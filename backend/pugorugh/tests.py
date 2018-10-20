from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from . import models
from . import serializers
from . import views


class UserAPITests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = models.User.objects.create(username='test', password='test')
        self.user_pref = models.UserPref.objects.create(user=self.user, gender='m', age=2, size='sml')

    def test_create_new_user(self):
        """
        Ensure we can register a new user.
        """

        new_user_data = {
            'username': 'test2',
            'password': 'test2',
        }

        request = self.factory.post(reverse('register-user'), new_user_data)

        view = views.UserRegisterView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.User.objects.count(), 2)
        self.assertEqual(models.User.objects.get(pk=2).username, 'test2')

    def test_get_user_pref(self):
        """
        Ensure we can get user preferences using signed in user data.
        """

        request = self.factory.get(reverse('preferences-user'))
        force_authenticate(request, user=self.user)

        view = views.UserPrefView.as_view()
        response = view(request)

        serializer = serializers.UserPrefSerializer(self.user_pref)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_user_pref(self):
        """
        Ensure we can put new user data based on signed in user data.
        """

        new_user_pref_data = {
            'gender': 'f',
            'age': 1,
            'size': 'l',
        }

        request = self.factory.put(reverse('register-user'), new_user_pref_data)
        force_authenticate(request, user=self.user)

        view = views.UserPrefView.as_view()
        response = view(request)

        serializer = serializers.UserPrefSerializer(models.UserPref.objects.get())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class DogAPITests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = models.User.objects.create(username='test', password='test')
        self.dog = models.Dog.objects.create(
            name='Muffin',
            image_filename='3.jpg',
            breed='Boxer',
            age=24,
            gender='f',
            size='xl'
        )
        self.user_dog = models.UserDog.objects.create(
            user=self.user,
            dog=self.dog,
            status='l'
        )

    def test_create_dog(self):
        """
        Ensure we can create a new dog object.
        """

        new_dog_data = {
            'name': 'Hank',
            'image_filename': '2.jpg',
            'breed': 'French Bulldog',
            'age': 14,
            'gender': 'm',
            'size': 's'
        }

        request = self.factory.post(reverse('dog-list'), new_dog_data)
        force_authenticate(request, user=self.user)

        view = views.DogListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Dog.objects.count(), 2)
        self.assertEqual(models.Dog.objects.get(pk=2).name, 'Hank')

    def test_delete_dog(self):
        """
        Ensure we can delete dog object.
        """

        request = self.factory.delete(reverse('dog-detail-delete', kwargs={'pk': 1}))
        force_authenticate(request, user=self.user)

        view = views.DogDetailDeleteView.as_view()
        response = view(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Dog.objects.count(), 0)

    def test_get_dog_list(self):
        """
        Ensure we can get a correct list of dogs.
        """

        models.Dog.objects.create(
            name='Francesca',
            image_filename='1.jpg',
            breed='Labrador',
            age=72,
            gender='f',
            size='l'
        )

        request = self.factory.get(reverse('dog-list'))
        force_authenticate(request, user=self.user)

        view = views.DogListView.as_view()
        response = view(request)

        serializer = serializers.DogSerializer(models.Dog.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_dog_status_list(self):
        """
        Ensure we can get a correct list of dogs filtered by user dog status.
        """

        dog = models.Dog.objects.create(
            name='Francesca',
            image_filename='1.jpg',
            breed='Labrador',
            age=72,
            gender='f',
            size='l'
        )
        self.user_dog = models.UserDog.objects.create(
            user=self.user,
            dog=dog,
            status='l'
        )

        request = self.factory.get(reverse('dog-status-list', kwargs={'status': 'liked'}))
        force_authenticate(request, user=self.user)

        view = views.DogStatusListView.as_view()
        response = view(request, status='liked')

        serializer = serializers.DogSerializer(models.Dog.objects.filter(userdog__status='l'), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_dog_detail_next(self):
        """
        Ensure we can get a correct dog when it is liked.
        """

        new_dog = models.Dog.objects.create(
            name='Francesca',
            image_filename='1.jpg',
            breed='Labrador',
            age=72,
            gender='f',
            size='l'
        )
        new_user_dog = models.UserDog.objects.create(
            user=self.user,
            dog=new_dog,
            status='l'
        )

        request = self.factory.get(reverse('dog-detail-next', kwargs={'pk': 1, 'status': 'liked'}))
        force_authenticate(request, user=self.user)

        view = views.DogGetNextView.as_view()
        response = view(request, pk=1, status='liked')

        serializer = serializers.DogSerializer(new_dog)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_dog_detail_next_bad_data(self):
        """
        Ensure we can get the correct status code with a bad status passed.
        """

        request = self.factory.get(reverse('dog-detail-next', kwargs={'pk': -1, 'status': 'bad'}))
        force_authenticate(request, user=self.user)

        view = views.DogGetNextView.as_view()
        response = view(request, pk=1, status='bad')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_dog_detail(self):
        """
        Ensure that we can change a dog's status with put.
        """

        request = self.factory.put(reverse('dog-detail-custom', kwargs={'pk': 1, 'status': 'disliked'}))
        force_authenticate(request, user=self.user)

        view = views.DogDetailUpdateView.as_view()
        response = view(request, pk=1, status='disliked')

        user_dog = models.UserDog.objects.get(pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_dog.status, 'd')
