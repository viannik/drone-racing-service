from datetime import timedelta

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.country})"

    def get_absolute_url(self):
        return reverse(
            "racing:manufacturer-detail",
            kwargs={"pk": self.pk},
        )


class Drone(models.Model):
    model_name = models.CharField(
        max_length=255,
    )
    max_speed = models.FloatField(
        help_text="Max speed in km/h",
        validators=[MinValueValidator(0.0)]
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Weight in kg",
        validators=[MinValueValidator(0.0)]
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name="drones",
    )
    pilots = models.ManyToManyField(
        "accounts.Pilot",
        related_name="drones",
        blank=True,
    )

    class Meta:
        ordering = ["model_name", "manufacturer"]
        unique_together = ("model_name", "manufacturer")

    def __str__(self):
        return f"{self.model_name} ({self.manufacturer.name})"

    def get_absolute_url(self):
        return reverse(
            "racing:drone-detail",
            kwargs={"pk": self.pk},
        )


class RaceTrack(models.Model):
    DIFFICULTY_CHOICES = [
        (1, "Beginner"),
        (2, "Intermediate"),
        (3, "Advanced"),
        (4, "Expert"),
        (5, "Professional"),
    ]

    name = models.CharField(
        max_length=255,
        unique=True,
    )
    difficulty_level = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        default=1,
    )
    length_meters = models.IntegerField(
        help_text="Length in meters",
    )
    location = models.CharField(
        max_length=255,
        help_text="Race track location",
    )
    record_time = models.DurationField(
        verbose_name="Record Time (HH:MM:SS)",
        null=True,
        blank=True,
        help_text="Enter the record time in hours:minutes:seconds ",
        validators=[MinValueValidator(timedelta(seconds=0))],
    )

    class Meta:
        ordering = ["difficulty_level", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_difficulty_level_display()})"

    def get_absolute_url(self):
        return reverse(
            "racing:racetrack-detail",
            kwargs={"pk": self.pk},
        )