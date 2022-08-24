from django import forms
from .models import IngredientItem


class InputForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    roll_number = forms.IntegerField(
        help_text="Enter 6 digit roll number"
    )


class IngredientItemForm(forms.ModelForm):
    # store_name = forms.CharField(max_length=200, required=True, choices)
    # store_name = forms.ModelChoiceField(Store.objects.all().values_list('store_name', flat=True), initial=0)

    class Meta:
        model = IngredientItem
        fields = ['barcode', 'name', 'description']


class BarcodeScanner(forms.Form):
    barcode = forms.CharField(max_length=50, required=True)
    # quantity = forms.FloatField(required=True)
