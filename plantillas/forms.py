from django import forms
from .models import plantillaModel
# from django_summernote.widgets import SummernoteInplaceWidget


class plantillaForm(forms.ModelForm):
    public = forms.TypedChoiceField(widget=forms.RadioSelect, coerce=int,
                                    choices=[(0, "Privado"),
                                             (1, "Publico")])

    class Meta:
        model = plantillaModel
        widgets = {
             # 'summernote': SummernoteInplaceWidget(),
             'doc_id': forms.TextInput(attrs={'readonly': 'readonly'}),
             'creation_date': forms.DateInput(format='%d-%m-%Y'),
        }

        fields = ('summernote', 'title', 'description',
                  'public', 'tags')
