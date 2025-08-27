from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    RegexValidator,)
from django.db import models
from django.urls import reverse


class Pilot(AbstractUser):
    drone_license = models.CharField(
        max_length=8, 
        unique=True,
        validators=[
            RegexValidator(
                regex='^[A-Z0-9]{8}$',
                message='License must be 8 characters long and '
                        'contain only uppercase letters and numbers.',
            ),
        ],
    )
    skill_rating = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
    )
    certification_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "pilot"
        verbose_name_plural = "pilots"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} (Rating: {self.skill_rating})"

    def get_absolute_url(self):
        return reverse("pilots:pilot-detail", kwargs={"pk": self.pk})
