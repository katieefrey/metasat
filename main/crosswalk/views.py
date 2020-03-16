from django.shortcuts import render
from django.http import HttpResponse

from .models import ExternalSchema, ExternalElement

# Create your views here.

def index(request):

    allcrosswalks = ExternalSchema.objects.all()

    context = {"allcrosswalks": allcrosswalks}

    return render(request, "crosswalk/index.html", context)



def crosswalk(request,crosswalk):

    cw = ExternalSchema.objects.get(name=crosswalk)

    cwid = cw.id
    print(cwid)

    terms = ExternalElement.objects.filter(source=cwid)
    
    print(terms)
    context = {"terms": terms,
                "crosswalk": cw.name}

    return render(request, "crosswalk/crosswalk.html", context)