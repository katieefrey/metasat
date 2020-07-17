from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .models import Element, ElementFamily, Segment
from .forms import ElementForm, FamComp, SegComp
from crosswalk.forms import ExternalElementForm, ExElFormSet
from crosswalk.models import ExternalElement

# from django.forms import modelformset_factory

import string

def index(request):

    view = request.GET.get('view', '')

    if view == "family":

        all_fams = ElementFamily.objects.order_by('family')

        fams = {}
        for x in all_fams:
            fams[x] = Element.objects.filter(family=x).order_by('identifier')
        

        context = {
            "fams" : fams,
                }

        return render(request, "metasat/family.html", context)

    elif view == "segment":

        all_segs = Segment.objects.order_by('segment')

        segs = {}
        for x in all_segs:
            segs[x] = Element.objects.filter(segment=x).order_by('identifier')

        context = {
            "segs" : segs,
                }

        return render(request, "metasat/segment.html", context)

    else:

        alphabet = list(string.ascii_lowercase)
        all_elements = Element.objects.order_by('identifier')

        context = {
                    "all_elements" : all_elements,
                    "alphabet" : alphabet,
                }
        
        return render(request, "metasat/element.html", context)


def element(request,element):

    try:

        el = Element.objects.get(identifier=element)

        elid = el.id
        crosswalks = ExternalElement.objects.filter(metasat_element_id=elid)

        context = {
                    "element": el,
                    "crosswalks": crosswalks,
                }
    

    except Element.DoesNotExist:
        context = {"element": element}
        return render(request, "metasat/unknown.html",context)
    
    family = request.GET.get('family','')
    segment = request.GET.get('segment','')
    
    if family != '':    

        all_fams = ElementFamily.objects.order_by('family')
        fams = {}
        for x in all_fams:
            fams[x] = Element.objects.filter(family=x).order_by('identifier')

        context["fams"] = fams
        

        return render(request, "metasat/family.html", context)
    
    elif segment != '':    

        all_segs = Segment.objects.order_by('segment')
        segs = {}
        for x in all_segs:
            segs[x] = Element.objects.filter(segment=x).order_by('identifier')

        context["segs"] = segs

        return render(request, "metasat/segment.html", context)

    else:

        alphabet = list(string.ascii_lowercase)
        all_elements = Element.objects.order_by('identifier')
        context["all_elements"] = all_elements
        context["alphabet"] = alphabet

        return render(request, "metasat/element.html", context)


def edit(request,element):
    print("on the edit page!")
    try:

        el = Element.objects.get(identifier=element)

        elid = el.id
        print(el.family)

        crosswalks = ExternalElement.objects.filter(metasat_element_id=elid)
        
        famcomp = FamComp(instance=Element.objects.get(identifier=element))
        segcomp = SegComp(instance=Element.objects.get(identifier=element))
        elform = ElementForm(instance=Element.objects.get(identifier=element))

        exelform = ExternalElementForm()

        exelformset = ExElFormSet(queryset=ExternalElement.objects.filter(metasat_element_id=elid))

        # for form in exelformset:
        #     print(form.as_table())

        #context["elform"] = elform
        context = {"element": el,
                   "crosswalks": crosswalks,
                   "elform" : elform,
                   "famcomp" : famcomp,
                   "segcomp" : segcomp,
                   "exelform" : exelform,
                   "exelformset": exelformset,
                    }

    except Element.DoesNotExist:
        context = {"element": element}
        return render(request, "metasat/unknown.html",context)

    return render(request, "metasat/edit.html", context)


def update(request):

    if not request.user.is_authenticated:
        context = {
            "state": "home",
            "error": "Please login and try again."
            }
        return render(request, "metasat/index.html", context)

    #otherwise, if they are logged in...
    username = request.user
    userid = username.id

    try:

        fams = request.POST.getlist('family')
        segs = request.POST.getlist('segment')

        #loc = request.POST["location"]
        elid = request.POST["elid"]

        syn = request.POST['synonym']
        ex = request.POST['example']
        desc = request.POST['desc']
        source = request.POST['source']

        myElement = Element.objects.get(id=elid)
        
        myElement.family.clear()
        for x in fams:
            myElement.family.add(x)

        myElement.segment.clear()
        for x in segs:
            myElement.segment.add(x)


        #myElement.location_id = loc

        myElement.synonym = syn
        myElement.example = ex
        myElement.desc = desc
        myElement.source = source

        myElement.save()

        context = {
            "item" : myElement
        }

        return HttpResponseRedirect('%s' % myElement.identifier)

    except Element.DoesNotExist:

        context = {
            "state": "loggedin",
            "error": "Item not found, try again."
            }
        return render(request, "metasat/index.html", context)


# #foundation
# def index2(request):

#     all_elements = Element.objects.order_by('identifier')

#     alphabet = list(string.ascii_lowercase)

#     context = {
#         "all_elements": all_elements,
#         "alphabet": alphabet
#             }

#     return render(request, "metasat/index2.html", context)


# # more bootstrap
# def index3(request):

#     all_elements = Element.objects.order_by('identifier')

#     alphabet = list(string.ascii_lowercase)

#     context = {
#         "all_elements": all_elements,
#         "alphabet": alphabet
#             }

#     return render(request, "metasat/index3.html", context)


# # from scratch?
# def index4(request):

#     all_elements = Element.objects.order_by('identifier')

#     alphabet = list(string.ascii_lowercase)

#     context = {
#         "all_elements": all_elements,
#         "alphabet": alphabet
#             }

#     return render(request, "metasat/index4.html", context)


# # more bootstrap
# def alpha(request):

#     all_elements = Element.objects.order_by('identifier')

#     alphabet = list(string.ascii_lowercase)

#     context = {
#         "all_elements": all_elements,
#         "alphabet": alphabet
#             }

#     return render(request, "metasat/metasat4.html", context)


# # more bootstrap
# def family(request):


#     # ?hours=sunday&map=flash
#     #hours = request.GET.get('hours', '')
#     #map = request.GET.get('map', '')
#     #127.0.0.1:8000/metasat/2/accelerometer?view=family&family=AttitudeControl

#     all_elements = Element.objects.order_by('identifier')

#     all_fams = ElementFamily.objects.order_by('family')
#     fams = {}
#     for x in all_fams:
#         fams[x] = Element.objects.filter(family=x).order_by('identifier')

#     context = {
#         "fams" : fams,
#         "all_elements": all_elements,
#             }

#     return render(request, "metasat/family.html", context)

# # more bootstrap
# def segment(request):

#     all_elements = Element.objects.order_by('identifier')

#     alphabet = list(string.ascii_lowercase)

#     context = {
#         "all_elements": all_elements,
#         "alphabet": alphabet
#             }

#     return render(request, "metasat/segment.html", context)


