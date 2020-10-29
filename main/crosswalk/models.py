from django.db import models
from metasat.models import Element

class ExternalSchema(models.Model):

    # url safe identifier
    identifier = models.CharField(max_length=255, null=True, blank=True)

    # name can include accent marks and diacritics
    name = models.CharField(max_length=255)

    # url of the overall schema, not being used
    url = models.CharField(max_length=255, null=True, blank=True)

    # language code for schema title to assit with screen readers
    # NOT language of the vocab itself
    lang = models.CharField(max_length=4, null=True, blank=True)

    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


# assumes each external element only has one relationship to a metasat element
class ExternalElement(models.Model):
    identifier = models.CharField(max_length=255)
    label = models.CharField(max_length=50, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    source = models.ForeignKey(ExternalSchema, on_delete=models.CASCADE, null=True, blank=True)
    metasatelement = models.ForeignKey(Element, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.source}: {self.identifier}"

    class Meta:
       ordering = ('metasatelement',)