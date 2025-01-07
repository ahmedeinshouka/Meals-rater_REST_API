from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver




class Meal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    # A text field to store additional comments or feedback about the meal.
    # A text field to store additional comments or feedback about the rating.
    description = models.TextField()
    # The 'upload_to' parameter specifies the subdirectory within the media root where the image will be stored.
    image = models.ImageField(upload_to='meals/')
    # A date field to store the date when the meal was consumed.
    date = models.DateField()
    def __str__(self):
        return self.name


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # An integer field to store the rating, with a valid range from 1 to 5.
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()
    def __str__(self):
        return f'{self.meal.name} - {self.stars}'
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['meal', 'user'], name='unique_meal_user')
        ]
        indexes = [
            models.Index(fields=['user', 'meal']),
        ]
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
            
          
      



