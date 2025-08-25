from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Pilot(AbstractUser):
    drone_license = models.CharField(max_length=8, unique=True)
    skill_rating = models.IntegerField(default=1)
    certification_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "pilot"
        verbose_name_plural = "pilots"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} (Rating: {self.skill_rating})"

    def get_absolute_url(self):
        return reverse("accounts:pilot-detail", kwargs={"pk": self.pk})