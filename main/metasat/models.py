from django.db import models

class ElementFamily(models.Model):
    family = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.family}"


class Segment(models.Model):
    segment = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.segment}"

class Element(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    term = models.CharField(max_length=255)
    synonym = models.CharField(max_length=255, null=True, blank=True)
    example = models.TextField(null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    source = models.TextField(null=True, blank=True)
    family = models.ManyToManyField(ElementFamily, blank=True)
    segment = models.ManyToManyField(Segment, blank=True)

    def __str__(self):
        return f"{self.identifier}"


    class Meta:
       ordering = ('identifier',)