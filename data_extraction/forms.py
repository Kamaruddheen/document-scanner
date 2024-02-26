from django import forms

class FileUploadForm(forms.Form):
    input_file = forms.FileField()