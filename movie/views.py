from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import Http404

from movie.exception import PageNotAnInteger, LengthNotCorrect
from movie.utils import to_dict
from movie.validation import validate_number, validate_len
from movie.models import Genre, Movie


class GenresView(View):
    def get(self, request):
        data = list(Genre.objects.values("id", "title"))
        return JsonResponse(data, safe=False)


class MovieDetailView(View):
    def get(self, request, pk):
        try:
            data_obj = get_object_or_404(Movie, pk=pk)
        except Http404:
            return JsonResponse({"error": ["movie__not_found"]})
        movie_serializers = to_dict(data_obj, request)

        return JsonResponse(movie_serializers, safe=False)


class MoviesView(View):
    def get(self, request):
        movies = Movie.objects.prefetch_related(
            "genres", "directors", "writers", "stars"
        )

        genre_pk = request.GET.get("genre")
        if genre_pk:
            try:
                get_object_or_404(Genre, pk=genre_pk)
            except (Http404, ValueError):
                return JsonResponse({"error": ["genre__invalid"]})

            movies = movies.filter(genres__id=genre_pk)

        src = request.GET.get("src")
        if src:
            try:
                validate_len(src)
            except LengthNotCorrect:
                return JsonResponse({"error": ["src__invalid"]})

            movies = movies.filter(title__startswith=src)

        page_number = request.GET.get("page")
        if page_number:
            try:
                page_number = validate_number(page_number)
            except PageNotAnInteger:
                return JsonResponse({"error": ["page__invalid"]})

        paginator = Paginator(movies, 1)
        page_obj = paginator.get_page(page_number)

        if page_number and int(page_number) > page_obj.paginator.num_pages:
            return JsonResponse({"error": ["page__out_of_bounds"]})

        results = [to_dict(obj, request) for obj in page_obj]

        serializers_data = {
            "results": results,
            "pages": page_obj.paginator.num_pages,
            "total": movies.count()
        }

        return JsonResponse(serializers_data, safe=False)
