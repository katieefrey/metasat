from django.shortcuts import render
from django.http import HttpResponse

from .models import Element, Segment
from crosswalk.models import ExternalElement

def index(request):

    all_elements = Element.objects.order_by('identifier')
    #ll_elements

    all_segs = Segment.objects.all()

    context = {"all_elements": all_elements,
                "all_segs": all_segs
            }

    return render(request, "metasat/index.html", context)


def element(request,element):

    try:

        el = Element.objects.get(identifier=element)

        segs = []
        for x in el.segment.all():
            segs.append(str(x))

        segments =  ", ".join(segs)

        elid = el.id

        crosswalks = ExternalElement.objects.filter(metasat_element_id=elid)

        context = {"element": el,
                    "segments": segments,
                    "crosswalks": crosswalks
                }
        

    except Element.DoesNotExist:
        context = {"element": element}
        return render(request, "metasat/unknown.html",context)
        
    
    

    return render(request, "metasat/metasat.html", context)

