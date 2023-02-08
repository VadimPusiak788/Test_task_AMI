from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Date(models.Model):
    create_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Genre(Date):
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title


class Person(Date):
    class TypePeople(models.TextChoices):
        Director = "DR", "Director"
        Writer = "WR", "Writer"
        Actor = "AC", "Actor"

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    types = models.CharField(
        max_length=2, choices=TypePeople.choices, default=TypePeople.Actor
    )

    def __str__(self) -> str:
        return f"{self.first_name}  {self.last_name}"


class Movie(Date):
    GENERAL = "G"
    PARENTAL_GUIDANCE = "PG"
    PARENTS_STRONGLY = "PG-13"
    RESTRICTED = "R"
    ADULTS = "NC-17"

    RATE_CHOICES = [
        (GENERAL, "General Audiences"),
        (PARENTAL_GUIDANCE, "Parental Guidance Suggested"),
        (RESTRICTED, "Restricted"),
        (ADULTS, "Adults Only"),
    ]

    title = models.CharField(max_length=50)
    description = models.TextField()
    poster = models.ImageField(upload_to="poster")
    bg_picture = models.ImageField(upload_to="big_picture")
    release_year = models.IntegerField(
        validators=[MinValueValidator(1200), MaxValueValidator(2023)]
    )
    mpa_rating = models.CharField(max_length=5, choices=RATE_CHOICES, default="")
    imdb_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.01), MaxValueValidator(10)],
    )
    duration = models.IntegerField(validators=[MinValueValidator(0.01)])
    genres = models.ManyToManyField(Genre)
    directors = models.ManyToManyField(Person, related_name="directors")
    writers = models.ManyToManyField(Person, related_name="writers")
    stars = models.ManyToManyField(Person, related_name="stars")

    def __str__(self) -> str:
        return self.title
