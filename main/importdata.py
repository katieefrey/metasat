# standard lib packages
import sys
import os
import requests
import json
import urllib.parse
import time
import csv
from openpyxl import Workbook

os.environ.setdefault('DJANGO_SETTINGS_MODULE','main.settings')

import django
django.setup()

from crosswalk.models import ExternalSchema, ExternalElement
from metasat.models import Element, Segment, ElementFamily

runwhat = input("What do you want to import?\n\n  1) Elements Only\n  2) Crosswalks Only\n  3) Elements AND Crosswalks\n\n  4) Remind me about the file format requirements\n\nPlease enter 1, 2, 3, or 4: ")

## add item functions

def add_Segment(data1):
    d, created = Segment.objects.get_or_create(segment=data1)
    return d

def add_Family(data1):
    d, created = ElementFamily.objects.get_or_create(family=data1)
    return d

def add_ExternalSchema(data1):
    d, created = ExternalSchema.objects.get_or_create(name=data1)
    return d

def add_ExternalElement(data1, data3, data4, data5):
    d, created = ExternalElement.objects.get_or_create(identifier=data1, url=data3, source_id=data4, metasatelement_id=data5)

    return d

def add_Element(data1, data2, data3, data4, data5, data6, segments, families):

    e1, created = Element.objects.get_or_create(identifier=data1, term=data2, desc=data3, synonym=data4, example=data5, source=data6)
    e1.save()

    for x in segments:
        e1.segment.add(x)

    for x in families:
        e1.family.add(x)
    e1.save()


# def update_Element(data1, data2, data3, data4, data5, data6, segments, families):
#     d = Element.objects.get(identifier=data1)
#     d.term = data2 
#     d.desc = data3
#     d.synonym = data4
#     d.example = data5
#     d.source = data6

#     d.segment.clear()
#     for x in segments:
#         d.segment.add(x)

#     d.family.clear()
#     for x in families:
#         d.family.add(x)
#     d.save()



######### adding elements

def importelements(elfile):

    Element.objects.all().delete()
    ElementFamily.objects.all().delete()
    Segment.objects.all().delete()

    from openpyxl import load_workbook

    wb = load_workbook(filename = elfile)


    #wb_obj = openpyxl.load_workbook(path) 
      
    # Get workbook active sheet object 
    # from the active attribute 
    sheet_obj = wb.active 
      
    # Cell objects also have row, column,  
    # and coordinate attributes that provide 
    # location information for the cell. 
      
    # Note: The first row or  
    # column integer is 1, not 0. 
      
    # Cell object is created by using  
    # sheet object's cell() method. 
    cell_obj = sheet_obj.cell(row = 2, column = 5) 
      
    # Print value of cell object  
    # using the value attribute 
    #print(cell_obj.value) 

    # sheet_ranges = wb['Term','Identifier']
    # print(sheet_ranges['D18'].value)

    num = sheet_obj.max_row

    for x in range(1,num+1):

        term = sheet_obj.cell(row = x, column = 2)
        identifier = sheet_obj.cell(row = x, column = 1)
        families = sheet_obj.cell(row = x, column = 4) 
        segments = sheet_obj.cell(row = x, column = 5) 
        desc = sheet_obj.cell(row = x, column = 6) 
        example = sheet_obj.cell(row = x, column = 7)
        synonyms = sheet_obj.cell(row = x, column = 3)
        source = sheet_obj.cell(row = x, column = 8)


        familys = (families.value).split(", ")
        fam = []
        for x in familys:
           z = add_Family(x.strip())
           fam.append(z)

        segs1 = (segments.value).split(", ")
        seg = []
        for x in segs1:
            z = add_Segment(x)
            seg.append(z)

        print (identifier.value)
        add_Element((identifier.value).strip(),term.value,desc.value,synonyms.value,example.value,source.value, seg, fam)



############ adding crosswalks
def importcrosswalks(cwfile):

    ExternalSchema.objects.all().delete()
    ExternalElement.objects.all().delete()

    import pandas

    with open(cwfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = 0
        col_list = []
        name_list = []
        lang_list = []

        for row in csv_reader:
            if header == 0:

                for title in row:
                    #print (title)
                    col_list.append(title)
                header = 1
            elif header == 1:

                for name in row:
                    name_list.append(name)
                header = 2
            elif header == 2:

                for lang in row:
                    lang_list.append(lang)
                header = 3
            else:
                pass



        elementid = col_list[0]       

        new_list = col_list[1:]

        nameread = name_list[1:]
        langread = lang_list[1:]

        print (new_list)

        df = pandas.read_csv("crosswalk3.csv", encoding = "ISO-8859-1", usecols=col_list, skiprows=[1,3])

        num = 0
        for y in new_list:
            #add_ExternalSchema(y)
            print (y)
            count = 0
            for x in df[y]:
                if pandas.isnull(x):
                    pass
                else:
                    schema = ExternalSchema.objects.get(name=y)
                    #schema.identifier = (nameread[num]).replace(' ','-')
                    schema.lang = (langread[num])
                    schema.save()
                    #print(x) # vocab id & url
                    #print(df[elementid][count]) # elementid

                    # if str(x).startswith("http"):
                    #     uri = x
                    # else:
                    #     uri = None
                    # elid = Element.objects.get(identifier=df[elementid][count])
                    # add_ExternalElement(str(x), uri, schema.id, elid.id)
                count+=1
            num+=1




if runwhat == str(1):
    elfile = input("elements filename? must be .xlsx! ")
    importelements(elfile)
    print ("finished!")

elif runwhat == str(2):
    cwfile = input("crosswalk filename? must be .csv! ")
    importcrosswalks(cwfile)
    print ("finished!")

elif runwhat == str(3):
    elfile = input("elements filename? must be .xlsx! ")
    cwfile = input("crosswalk filename? must be .csv! ")
    importelements(elfile)
    importcrosswalks(cwfile)
    print ("finished!")

elif runwhat == str(4):

    print("the element files must be .xlsx")
    print("the crosswalk file must be .csv")

else:
    print("invalid entry rerun script")


