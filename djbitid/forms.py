from django import forms

class BitIdForm(forms.Form):
    """
    """

    uri = forms.CharField()
    address = forms.CharField()
    signature = forms.CharField()
