from django.db import models
from metasat.models import Element

class ExternalSchema(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


# class ExternalRelationshipSchema(models.Model):
#     name = models.CharField(max_length=50)
#     url = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.name}"


# class Relationship(models.Model):
#     predicate = models.CharField(max_length=50)
#     source = models.ForeignKey(ExternalRelationshipSchema, on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self):
#         return f"{self.predicate}"


# assumes each external element only has one relationship to a metasat element
class ExternalElement(models.Model):
    identifier = models.CharField(max_length=255)
    label = models.CharField(max_length=50, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    source = models.ForeignKey(ExternalSchema, on_delete=models.CASCADE, null=True, blank=True)
    #relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE, null=True, blank=True)
    metasat_element = models.ForeignKey(Element, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.source}: {self.identifier}"
