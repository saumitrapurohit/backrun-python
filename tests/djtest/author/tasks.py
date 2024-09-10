from backrun_sdk import task
from .models import Author


@task
def author_count():
    return Author.objects.all().count()


@task
def exception_raiser():
    raise Exception("This is an exception from exception_raiser")
