from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .models import Element, ElementFamily, Segment
from .forms import ElementForm, FamComp, SegComp
from crosswalk.forms import ExternalElementForm, ExElFormSet
from crosswalk.models import ExternalElement

from django.db.models import Q

import string


def index(request):

    view = request.GET.get('view', '')

    families = ElementFamily.objects.order_by('family')
    segments = Segment.objects.order_by('segment')

    all_elements = Element.objects.filter(deprecated=False).order_by('identifier').only('identifier')

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
            # "element" : "noelement"
            }

    if view == "family":
        context["gtype"] = "family"

    elif view == "segment":
        context["gtype"] = "segment"

    elif view == "search":
        lookup = (request.GET.get('lookup', '')).lower()

        context["gtype"] = "search"
        context["lookup"] = lookup

        if lookup != "":
            tlookup = lookup.title()
            clookup = lookup.capitalize() 
            ulookup = lookup.upper()

            res = Element.objects.filter( Q(term__icontains=lookup) | Q(synonym__icontains=lookup))

            for x in res:

                ident = x.identifier
                term = x.term
                syn = x.synonym

                if lookup in term:
                    x.term = term.replace(lookup,"<mark>"+lookup+"</mark>")
                    x.synonym = None
                elif tlookup in term:
                    x.term = term.replace(tlookup,"<mark>"+tlookup+"</mark>")
                    x.synonym = None
                elif clookup in term:
                    x.term = term.replace(clookup,"<mark>"+clookup+"</mark>")
                    x.synonym = None
                elif ulookup in term:
                    x.term = term.replace(ulookup,"<mark>"+ulookup+"</mark>")
                    x.synonym = None
                else:
                    if lookup in syn:
                        x.synonym = syn.replace(lookup,"<mark>"+lookup+"</mark>")
                    elif tlookup in syn:
                        x.synonym = syn.replace(tlookup,"<mark>"+tlookup+"</mark>")
                    elif clookup in syn:
                        x.synonym = syn.replace(clookup,"<mark>"+clookup+"</mark>")
                    elif ulookup in syn:
                        x.synonym = syn.replace(ulookup,"<mark>"+ulookup+"</mark>")
                    else:
                        pass

            context["results"] = res            
            context["clookup"] = clookup
            context["ulookup"] = ulookup
            context["tlookup"] = tlookup

    else:
        context["gtype"] = "alpha"
        
    return render(request, "metasat/index.html", context)


def element(request,element):

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

    try:
        el = Element.objects.get(identifier=element)
        crosswalks = ExternalElement.objects.filter(metasatelement_id=el.id).select_related('source')
        context["known"] = "yes"
        context["element"] = el
        context["crosswalks"] = crosswalks
    except Element.DoesNotExist:
        context["element"] = element
        context["known"] = "no"

    return render(request, "metasat/index.html", context)



def edit(request,element):
    try:
        el = Element.objects.get(identifier=element)
    except Element.DoesNotExist:
        context = {"element": element}
        return render(request, "metasat/unknown.html",context)

    elid = el.id

    crosswalks = ExternalElement.objects.filter(metasatelement_id=elid)
    
    famcomp = FamComp(instance=Element.objects.get(identifier=element))
    segcomp = SegComp(instance=Element.objects.get(identifier=element))
    elform = ElementForm(instance=Element.objects.get(identifier=element))

    exelform = ExternalElementForm()

    exelformset = ExElFormSet(queryset=ExternalElement.objects.filter(metasatelement_id=elid))

    context = {
                "element": el,
                "crosswalks": crosswalks,
                "elform" : elform,
                "famcomp" : famcomp,
                "segcomp" : segcomp,
                "exelform" : exelform,
                "exelformset": exelformset,
                }

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