from django.shortcuts import render
from django.http import HttpResponse

from .models import ExternalSchema, ExternalElement

# Create your views here.

def index(request):

    allcrosswalks = ExternalSchema.objects.all()
    context = {"allcrosswalks": allcrosswalks}

    return render(request, "crosswalk/index.html", context)



def crosswalk(request,crosswalk):

    cw = ExternalSchema.objects.get(identifier=crosswalk)
    terms = ExternalElement.objects.filter(source=cw.id)#.order_by('metasat_element')

    context = {"terms": terms,
                "crosswalk": cw.name}

    return render(request, "crosswalk/crosswalk.html", context)