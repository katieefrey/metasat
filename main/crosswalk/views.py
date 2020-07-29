from django.shortcuts import render
from django.http import HttpResponse

from .models import ExternalSchema, ExternalElement

# Create your views here.

def index(request):

    allcrosswalks = ExternalSchema.objects.all()
    context = {"allcrosswalks": allcrosswalks}

    return render(request, "crosswalk/index.html", context)



def crosswalk(request,crosswalk):

    allcrosswalks = ExternalSchema.objects.all()

    cw = ExternalSchema.objects.get(identifier=crosswalk)
    
    print ("step1")

    #terms = ExternalElement.objects.filter(source=cw.id, metasatelement_deprecated=False)

    terms = ExternalElement.objects.filter(source=cw.id).exclude(metasatelement__deprecated=True)

    print(terms)
    print ("step2")
    walkterms = []
    print ("step3")
    # for term in terms:
    #     if term.metasatelement.deprecated == False:
    #         newterm = {
    #             "element" : term.metasatelement,
    #             "url" : term.url,
    #             "id" : term.identifier,
    #         }

    #         walkterms.append(newterm)
    #     else:
    #         print ("this is deprecated")
    #         print(term)


    # #print (walkterms)
    # print ("step4")

    context = {
                "allcrosswalks": allcrosswalks,
                "terms": terms,
                "walkterms" : walkterms,
                "crosswalk": cw.name
            }

    return render(request, "crosswalk/index.html", context)