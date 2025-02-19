from drf_spectacular.utils import inline_serializer
from rest_framework.serializers import CharField


def not_found_404(class_name):
    return inline_serializer(
        f"{class_name}DoesNotExist",
        {"detail": CharField(default=f"No {class_name} matches the given query")},
    )


def authentication_401():
    return inline_serializer(
        "Unauthorized",
        {"detail": CharField(default="Authentication credentials were not provided.")},
    )


def bad_request_400():
    return inline_serializer(
        "BadRequest",
        {
            "field_name1": CharField(default="This field is required."),
            "field_name2": CharField(default="A valid {type} is required."),
            "non_field_errors": CharField(default="Validation error message"),
        },
    )
