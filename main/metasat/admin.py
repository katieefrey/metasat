from django.contrib import admin

from .models import Element, SchemaType, Segment

# Register your models here.
admin.site.register(Element)
admin.site.register(SchemaType)
admin.site.register(Segment)

