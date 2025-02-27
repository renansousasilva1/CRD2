from django import forms
from crud.models import noticia, Artigo


class NoticiaModelForm(forms.ModelForm):
    class Meta:
        model = noticia
        fields = '__all__'

class ArtigoModelForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = '__all__'

