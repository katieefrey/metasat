# standard lib packages
import sys
import os
import requests
import json
import urllib.parse
import time
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE','main.settings')

import django
django.setup()

from crosswalk.models import ExternalSchema, ExternalRelationshipSchema, Relationship, ExternalElement
from metasat.models import SchemaType, Segment, Element

## set up databases

def add_Segment(data1):
    d, created = Segment.objects.get_or_create(segment=data1)
    return d

## add_Segment("Ground Segment")
## add_Segment("Space Segment")
# add_Segment("Launch Segment")
# add_Segment("Mission Segment")
# add_Segment("Observation Segment")




def add_SchemaType(data1):
    d, created = SchemaType.objects.get_or_create(schematype=data1)
    return d

## add_SchemaType("Boolean")
# add_SchemaType("text")
# add_SchemaType("integer")


def add_ExternalSchema(data1):
    d, created = ExternalSchema.objects.get_or_create(name=data1,url=data2)
    return d

# add_ExternalSchema("wikidata","http://wikidata.org")


def add_ExternalRelationshipSchema(data1, data2):
    d, created = ExternalRelationshipSchema.objects.get_or_create(name=data1,url=data2)
    return d

#add_ExternalRelationshipSchema("skos","http://skos.org")

def add_Relationship(data1, data2):
    d, created = Relationship.objects.get_or_create(predicate=data1,source_id=data2)
    return d

#add_Relationship("broader",2)



## add content to databases


def add_ExternalElement(data1, data2, data3, data4, data5, data6):
    d, created = ExternalElement.objects.get_or_create(identifier=data1, label=data2, url=data3, source_id=data4, relationship_id=data5, metasat_element_id=data6)

    return d





def add_Element(data1, data2, data3, data4, data5, data6, segments):
    #d, created = Element.objects.get_or_create(identifier=data1, desc=data2, synonym=data3, example=data4, schematype_id=data5)


    e1 = Element(identifier=data1, desc=data2, synonym=data3, example=data4, schematype_id=data5, source=data6)
    e1.save()

    for x in segments:
        e1.segment.add(x)
    e1.save()










  
#add_Element("owner","Person or organization who owns the ground station","", "", 2, [s1,s2,s3])


s1 = Segment.objects.get(id=1) # Ground segment
s2 = Segment.objects.get(id=2) # Space segment
# s3 = Segment.objects.get(id=3) # Luanch segment
# s4 = Segment.objects.get(id=4) # Mission segment
# s5 = Segment.objects.get(id=5) # Observation segment



with open('metasat.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(row)

        atype = row[5]
        if atype == "Boolean":
            stype = 1
        else:
            stype = None

        segment = (row[6]).split(",")

        seg = []
        for x in segment:
            if x == "Ground Segment":
                seg.append(s1)
            if x == "Space Segment":
                seg.append(s2)


        print (seg)


        #add_Element(row[0],row[1],row[2],row[3],stype,row[5],seg)



# with open('crosswalk.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     for row in csv_reader:
#         print(row)

        #add_ExternalElement("P127","Owned by","https://www.wikidata.org/wiki/Property:P127",1,1,15)
        #add_ExternalElement(name, barcode, notes)


#     print ("finished!")