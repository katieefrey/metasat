from django import forms

from .models import Element

from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

class ElementForm(ModelForm):
    class Meta:
        model = Element
        fields = ('example','synonym','desc','source',)
        labels = {
            'desc': 'Description',
            'source': 'Source of Description',
            'example' : 'Examples',
            'synonym': 'Synonyms',
        }

    def __init__(self, *args, **kwargs):
        
        super(ElementForm, self).__init__(*args, **kwargs)

        
        self.fields['example'].widget = forms.Textarea(attrs={'rows': 1})
        self.fields['synonym'].widget = forms.Textarea(attrs={'rows': 1})
        self.fields['desc'].widget = forms.Textarea(attrs={'rows': 2})
        self.fields['source'].widget = forms.Textarea(attrs={'rows': 1})
        

class FamComp(ModelForm):
    
    class Meta:
        model = Element
        fields = ("family",)
        labels = {
            'family': 'Element Family',
        }
             
    def __init__(self, *args, **kwargs):
        
        super(FamComp, self).__init__(*args, **kwargs)
        self.fields["family"].widget = CheckboxSelectMultiple()
        


class SegComp(ModelForm):
    
    class Meta:
        model = Element
        fields = ("segment",)
        labels = {
            'segment': 'Segment',
        }
             
    def __init__(self, *args, **kwargs):
        
        super(SegComp, self).__init__(*args, **kwargs)
        self.fields["segment"].widget = CheckboxSelectMultiple()