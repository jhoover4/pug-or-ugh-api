from django.contrib.auth.models import User
from django.db import models
from django.db import IntegrityError


class Dog(models.Model):
    """A dog that is available for adoption."""

    MALE = 'm'
    FEMALE = 'f'
    UNKNOWN = 'u'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNKNOWN, 'Unknown'),
    )

    SMALL = 's'
    MEDIUM = 'm'
    LARGE = 'l'
    EXTRA_LARGE = 'xl'
    UNKNOWN = 'u'
    SIZE_CHOICES = (
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (EXTRA_LARGE, 'Extra Large'),
        (UNKNOWN, 'Unknown'),
    )

    name = models.CharField(max_length=200)
    image_filename = models.CharField(max_length=200)
    breed = models.CharField(max_length=200, null=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)

    def __str__(self):
        return self.name


class UserDog(models.Model):
    """Connects user preferences to their individual dog."""

    LIKED = 'l'
    DISLIKED = 'd'
    STATUS_CHOICES = (
        (LIKED, 'Liked'),
        (DISLIKED, 'Disliked'),
    )

    user = models.ForeignKey('auth.User')
    dog = models.ForeignKey('Dog', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            user_dog = UserDog.objects.filter(user=self.user, dog=self.dog)
            if user_dog.count() != 0:
                raise IntegrityError(
                    "UserDog item with same dog field exist on user_dog %r" % user_dog[0].pk
                )
        super(UserDog, self).save(*args, **kwargs)


class UserPref(models.Model):
    """User preferences for dog to adopt. Extends the user model."""

    user = models.ForeignKey('auth.User')

    # CharFields will be a string of comma-separated options that can be split to find values.
    gender = models.CharField(max_length=15)
    age = models.CharField(max_length=15)
    size = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
