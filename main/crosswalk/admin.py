from django.contrib import admin

from .models import ExternalSchema, ExternalElement#, Relationship, ExternalRelationshipSchema

admin.site.register(ExternalSchema)
admin.site.register(ExternalElement)
# admin.site.register(Relationship)
# admin.site.register(ExternalRelationshipSchema)
