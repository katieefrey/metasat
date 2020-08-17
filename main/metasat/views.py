from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .models import Element, ElementFamily, Segment
from .forms import ElementForm, FamComp, SegComp
from crosswalk.forms import ExternalElementForm, ExElFormSet
from crosswalk.models import ExternalElement

import string




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


@query_debugger
def index(request):

    view = request.GET.get('view', '')

    families = ElementFamily.objects.order_by('family')
    segments = Segment.objects.order_by('segment')

    all_elements = Element.objects.filter(deprecated=False).order_by('identifier').only('identifier')#

    famgroups = {}
    for x in families:
        famgroups[x] = Element.objects.filter(family=x,deprecated=False).order_by('identifier')

    seggroups = {}
    for x in segments:
        seggroups[x] = Element.objects.filter(segment=x,deprecated=False).order_by('identifier')

    alphabet = list(string.ascii_lowercase)
    
    context = {
            "famgroups" : famgroups, # all elements by family
            "seggroups" : seggroups, # all elements by segment
            "all_elements" : all_elements, # all elements
            "alphabet" : alphabet,
            "element" : "noelement"
            }

    if view == "family":
        context["gtype"] = "family"

    elif view == "segment":
        context["gtype"] = "segment"

    else:
        context["gtype"] = "alpha"
        
    return render(request, "metasat/elementindex.html", context)


    
    # list_of_families = ["observation", "communication", "electrical", "optics"]

    # list_of_elements = [
    #             {
    #                 "element": "airDensity",
    #                 "families": ["observation", "communication"]
    #             },
    #             {
    #                 "element": "camera",
    #                 "families": ["electrical", "optics"]
    #             },
    #             {
    #                 "element": "coating",
    #                 "families": ["communication", "optics"]
    #             },
    #             {
    #                 "element": "amplitude",
    #                 "families": ["observation", "electrical"]
    #             }

    #         ]

    # famgroups = {
    #                 "observation" : ["amplitude","airDensity"],
    #                 "optics" : ["camera", "coating"],
    #                 "communication" : ["airDensity", "coating"],
    #                 "electrical" : ["camera","amplitude"],
    #             }




@query_debugger
def element(request,element):

    print("how about this")
    try:

        el = Element.objects.get(identifier=element)

        elid = el.id
        crosswalks = ExternalElement.objects.filter(metasatelement_id=elid).select_related('source')
        print("am i here?")
        print(el)

    except Element.DoesNotExist:
        context = {"element": element}
        return render(request, "metasat/unknown.html",context)


    
    family = request.GET.get('family','')
    segment = request.GET.get('segment','')

    families = ElementFamily.objects.order_by('family')
    segments = Segment.objects.order_by('segment')

    famgroups = {}
    for x in families:
        famgroups[x] = Element.objects.filter(family=x,deprecated=False).order_by('identifier')

    seggroups = {}
    for x in segments:
        seggroups[x] = Element.objects.filter(segment=x,deprecated=False).order_by('identifier')


    alphabet = list(string.ascii_lowercase)
    all_elements = Element.objects.filter(deprecated=False).order_by('identifier')


    context = {
            "element": el,
            "crosswalks": crosswalks,
            "famgroups" : famgroups, # all elements by family
            "seggroups" : seggroups, # all elements by segment
            "all_elements" : all_elements, # all elements
            "alphabet" : alphabet,
            }
    
    if family != '':    

        context["gtype"] = "family"

    elif segment != '':    

        context["gtype"] = "segment"

    else:

        context["gtype"] = "alpha"

    
    return render(request, "metasat/elementindex.html", context)


def edit(request,element):
    print("on the edit page!")
    try:

        el = Element.objects.get(identifier=element)

        elid = el.id
        print(el.family)

        crosswalks = ExternalElement.objects.filter(metasatelement_id=elid)
        
        famcomp = FamComp(instance=Element.objects.get(identifier=element))
        segcomp = SegComp(instance=Element.objects.get(identifier=element))
        elform = ElementForm(instance=Element.objects.get(identifier=element))

        exelform = ExternalElementForm()

        exelformset = ExElFormSet(queryset=ExternalElement.objects.filter(metasatelement_id=elid))

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