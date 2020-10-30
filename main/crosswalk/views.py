from django.shortcuts import render
from django.http import HttpResponse

from .models import ExternalSchema, ExternalElement


def index(request):

    allcrosswalks = ExternalSchema.objects.all()
    context = {"allcrosswalks": allcrosswalks}

    return render(request, "crosswalk/index.html", context)


def crosswalk(request,crosswalk):

    allcrosswalks = ExternalSchema.objects.all()

    cw = ExternalSchema.objects.get(identifier=crosswalk)

    terms = ExternalElement.objects.filter(source=cw.id).exclude(metasatelement__deprecated=True).select_related('metasatelement')
    
    print (cw.desc)
    context = {
                "allcrosswalks": allcrosswalks,
                "terms": terms,
                "crosswalk": cw.name,
                "language" : cw.lang,
                "desc" : cw.desc,
            }

    return render(request, "crosswalk/index.html", context)