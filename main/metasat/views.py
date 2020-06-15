from django.shortcuts import render
from django.http import HttpResponse

from .models import Element, ElementFamily, Segment
from crosswalk.models import ExternalElement

import string

def index(request):

    view = request.GET.get('view', None)
    print(view)

    if view == "family":

        all_fams = ElementFamily.objects.order_by('family')
        all_elements = Element.objects.order_by('identifier')

        fams = {}
        for x in all_fams:
            fams[x] = Element.objects.filter(family=x).order_by('identifier')
        alphabet = list(string.ascii_lowercase)

        context = {
            "fams" : fams,
            "alphabet": alphabet
                }

        return render(request, "metasat/families.html", context)

    else:

        all_elements = Element.objects.order_by('identifier')

        alphabet = list(string.ascii_lowercase)

        context = {
            "all_elements": all_elements,
            "alphabet": alphabet
                }

        return render(request, "metasat/index.html", context)


def families(request):

    all_fams = ElementFamily.objects.order_by('family')
    all_elements = Element.objects.order_by('identifier')

    fams = {}
    for x in all_fams:
        fams[x] = Element.objects.filter(family=x).order_by('identifier')
    alphabet = list(string.ascii_lowercase)

    context = {
        "fams" : fams,
        "alphabet": alphabet
            }

    return render(request, "metasat/families.html", context)


def segments(request):

    all_segs = Segment.objects.order_by('segment')
    all_elements = Element.objects.order_by('identifier')

    segs = {}
    for x in all_segs:
        segs[x] = Element.objects.filter(segment=x).order_by('identifier')
    alphabet = list(string.ascii_lowercase)

    context = {
        "segs" : segs,
        "alphabet": alphabet
            }

    return render(request, "metasat/segments.html", context)

def element(request,element):

    try:

        el = Element.objects.get(identifier=element)

        elid = el.id
        print(el.family)

        crosswalks = ExternalElement.objects.filter(metasat_element_id=elid)

        context = {"element": el,
                    "crosswalks": crosswalks
                }
        

    except Element.DoesNotExist:
        context = {"element": element}
        return render(request, "metasat/unknown.html",context)

    return render(request, "metasat/metasat.html", context)



#foundation
def index2(request):

    all_elements = Element.objects.order_by('identifier')

    alphabet = list(string.ascii_lowercase)

    context = {
        "all_elements": all_elements,
        "alphabet": alphabet
            }

    return render(request, "metasat/index2.html", context)


# more bootstrap
def index3(request):

    all_elements = Element.objects.order_by('identifier')

    alphabet = list(string.ascii_lowercase)

    context = {
        "all_elements": all_elements,
        "alphabet": alphabet
            }

    return render(request, "metasat/index3.html", context)
