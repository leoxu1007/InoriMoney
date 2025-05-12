from django import forms


class UploadStdBillTemplateFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

class SelectConvertBillForm(forms.Form):
    bill_type = forms.ChoiceField(choices=[('1', 'JCB'), ('2', '楽天ANA')])
    bill_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))