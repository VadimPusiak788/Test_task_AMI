from django.http import JsonResponse

from django.db.models.fields.files import ImageFieldFile


def server_error(request, *args, **kwargs):
    data = {"error": ["internal"]}
    return JsonResponse(data)


def to_dict(instance, request=None) -> dict:
    opts = instance._meta
    data = {}
    exclude_field = ("types", "create_at", "updated_at")
    for field in opts.concrete_fields:
        if isinstance(field.value_from_object(instance), ImageFieldFile):
            photo_url = field.value_from_object(instance).url
            data[field.name] = request.build_absolute_uri(photo_url)
        elif field.name not in exclude_field:
            data[field.name] = field.value_from_object(instance)

    for field in opts.many_to_many:
        data[field.name] = [to_dict(i) for i in field.value_from_object(instance)]

    return data
