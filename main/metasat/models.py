from django.db import models

class SchemaType(models.Model):
    schematype = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.schematype}"

class Segment(models.Model):
    segment = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.segment}"


class Element(models.Model):
    identifier = models.CharField(max_length=50)
    desc = models.TextField(null=True, blank=True)
    synonym = models.CharField(max_length=255, null=True, blank=True)
    example = models.TextField(null=True, blank=True)
    schematype = models.ForeignKey(SchemaType, on_delete=models.CASCADE, null=True, blank=True)
    segment = models.ManyToManyField(Segment, blank=True)
    source = models.TextField(null=True, blank=True)
    #segment = models.ForeignKey(Segment, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.identifier}"