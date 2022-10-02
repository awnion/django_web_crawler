from django import forms


class CrawlerForm(forms.Form):
    url = forms.URLField(required=True)
