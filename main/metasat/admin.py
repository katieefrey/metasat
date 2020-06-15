from django.contrib import admin

from .models import Element, ElementFamily, Segment

# Register your models here.
admin.site.register(Element)
admin.site.register(ElementFamily)
admin.site.register(Segment)

