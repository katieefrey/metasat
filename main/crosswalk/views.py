from django.shortcuts import render
from django.http import HttpResponse

from .models import ExternalSchema, ExternalElement

# Create your views here.


from django.db import connection, reset_queries
import time
import functools

def query_debugger(func):

    @functools.wraps(func)
    def inner_func(*args, **kwargs):

        reset_queries()
        
        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func





def index(request):

    allcrosswalks = ExternalSchema.objects.all()
    context = {"allcrosswalks": allcrosswalks}

    return render(request, "crosswalk/index.html", context)


@query_debugger
def crosswalk(request,crosswalk):

    allcrosswalks = ExternalSchema.objects.all()

    cw = ExternalSchema.objects.get(identifier=crosswalk)

    terms = ExternalElement.objects.filter(source=cw.id).exclude(metasatelement__deprecated=True).select_related('metasatelement')
    
    context = {
                "allcrosswalks": allcrosswalks,
                "terms": terms,
                "crosswalk": cw.name
            }

    return render(request, "crosswalk/index.html", context)