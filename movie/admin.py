from django.contrib import admin

from movie.models import Genre, Movie, Person


admin.site.register(Person)
admin.site.register(Genre)
admin.site.register(Movie)
