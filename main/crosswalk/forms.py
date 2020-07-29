from django import forms
from django.forms import formset_factory
from django.forms import modelformset_factory

from .models import ExternalElement, ExternalSchema

from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple





class ExternalElementForm(ModelForm):
    class Meta:
        model = ExternalElement
        fields = ('identifier','url','source','metasatelement')
        # labels = {
        #     'desc': 'Description',
        #     'source': 'Source of Description',
        #     'example' : 'Examples',
        #     'synonym': 'Synonyms',
        # }

    def __init__(self, *args, **kwargs):
        
        super(ExternalElementForm, self).__init__(*args, **kwargs)

        
        self.fields['url'].widget = forms.Textarea(attrs={'rows': 1})


ExElFormSet = modelformset_factory(ExternalElement,form=ExternalElementForm, fields = ('identifier','url','source'), extra=2)



# formset = ExElFormSet(initial=[
#     {'url': 'http://schema.space',
#     'identifier': 'a concept',}
# ])

# class FamComp(ModelForm):
    
#     class Meta:
#         model = Element
#         fields = ("family",)
#         labels = {
#             'family': 'Element Family',
#         }
             
#     def __init__(self, *args, **kwargs):
        
#         super(FamComp, self).__init__(*args, **kwargs)
#         self.fields["family"].widget = CheckboxSelectMultiple()
        


# class SegComp(ModelForm):
    
#     class Meta:
#         model = Element
#         fields = ("segment",)
#         labels = {
#             'segment': 'Segment',
#         }
             
#     def __init__(self, *args, **kwargs):
        
#         super(SegComp, self).__init__(*args, **kwargs)
#         self.fields["segment"].widget = CheckboxSelectMultiple()



# class CrossWalkComp(ModelForm):
    
#     class Meta:
#         model = Element
#         fields = ("segment",)
#         labels = {
#             'segment': 'Segment',
#         }
             
#     def __init__(self, *args, **kwargs):
        
#         super(SegComp, self).__init__(*args, **kwargs)
#         self.fields["segment"].widget = CheckboxSelectMultiple()