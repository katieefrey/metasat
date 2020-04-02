from django.shortcuts import render
from django.http import HttpResponse

from pyld import jsonld
import json
import requests

# https://github.com/digitalbazaar/pyld


# Create your views here.

def index(request):

    url = "https://gitlab.com/metasat/metasat-schema/-/raw/master/Examples/QUBIK_EXAMPLE.jsonld"
    content = requests.get(url)
    k = json.loads(content.text)

    doc = k#["@graph"]


    url2 = "https://gitlab.com/metasat/metasat-schema/-/raw/master/Examples/QUBIK_EXAMPLE.jsonld"
    content2 = requests.get(url2)
    j = json.loads(content2.text)
   
    ctx = j["@context"]


    compacted = jsonld.compact(doc, ctx)
    expanded = jsonld.expand(compacted)

    comp = json.dumps(compacted)
    expa = json.dumps(expanded)

    context = {
        "compacted" : comp,
        "expanded" : expa
    }

    return render(request, "playground/index.html", context)