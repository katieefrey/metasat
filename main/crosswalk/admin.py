from django.contrib import admin

from .models import ExternalSchema, Relationship, ExternalElement, ExternalRelationshipSchema

admin.site.register(ExternalSchema)
admin.site.register(Relationship)
admin.site.register(ExternalElement)
admin.site.register(ExternalRelationshipSchema)
