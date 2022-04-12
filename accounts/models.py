from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    Experience_CHOICES = (
        ('0', '0-3 years'),('1', '3-5 years'),('2', '5-10 years'),('3', '10+ years'))
    experience = models.CharField(max_length=1, choices=Experience_CHOICES, default='0')

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)