from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .models import Element, ElementFamily, Segment
from .forms import ElementForm, FamComp, SegComp
from crosswalk.forms import ExternalElementForm, ExElFormSet
from crosswalk.models import ExternalElement

import string

def index(request):

    view = request.GET.get('view', '')

    if view == "family":

        all_groups = ElementFamily.objects.order_by('family')

        groups = {}
        for x in all_groups:
            groups[x] = Element.objects.filter(family=x,deprecated=False).order_by('identifier')
        

        context = {
            "groups" : groups, # all elements organized by family
            "gtype" : "family",
                }

        # even if the groups are renamed,
        #this template should be able to handle it
        return render(request, "metasat/grouping.html", context)

    elif view == "segment":

        all_groups = Segment.objects.order_by('segment')

        groups = {}
        for x in all_groups:
            groups[x] = Element.objects.filter(segment=x,deprecated=False).order_by('identifier')

        context = {
            "groups" : groups, # all elements organized by segment
            "gtype" : "segment",
                }

        return render(request, "metasat/grouping.html", context)

    else:

        alphabet = list(string.ascii_lowercase)
        all_elements = Element.objects.filter(deprecated=False).order_by('identifier')

        context = {
                    "all_elements" : all_elements,
                    "alphabet" : alphabet,
                }
        
        return render(request, "metasat/element.html", context)


def element(request,element):

    try:

        el = Element.objects.get(identifier=element)

        elid = el.id
        crosswalks = ExternalElement.objects.filter(metasatelement_id=elid).select_related('source')

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

        all_groups = ElementFamily.objects.order_by('family')
        groups = {}
        for x in all_groups:
            groups[x] = Element.objects.filter(family=x,deprecated=False).order_by('identifier')

        context["groups"] = groups
        context["groupname"] = family
        context["gtype"] = "family"

        return render(request, "metasat/grouping.html", context)

    elif segment != '':    

        all_groups = Segment.objects.order_by('segment')
        groups = {}
        for x in all_groups:
            groups[x] = Element.objects.filter(segment=x,deprecated=False).order_by('identifier')

        context["groups"] = groups
        context["groupname"] = segment
        context["gtype"] = "segment"

        return render(request, "metasat/grouping.html", context)

    else:

        alphabet = list(string.ascii_lowercase)
        all_elements = Element.objects.filter(deprecated=False).order_by('identifier')
        context["all_elements"] = all_elements
        context["alphabet"] = alphabet

        return render(request, "metasat/element.html", context)


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